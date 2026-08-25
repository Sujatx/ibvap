"""Live RTSP streaming from the Hi-Focus / Dahua HD-XVR-4801H1-H DVR.

Import it:

    from dvr import Camera

    cam = Camera(1)
    cam.start()
    frame = cam.read()          # 1920x1080 BGR, correct aspect, or None
    ...
    cam.stop()

Or run it:

    python dvr.py               # all 5 cameras in a grid
    python dvr.py -c 3          # one camera, large
    python dvr.py --tune        # re-apply best encoder settings to the DVR

Settings come from dvr.env next to this file.
"""
import argparse
import os
import threading
import time
from pathlib import Path
from urllib.parse import quote

import numpy as np

ENV_FILE = Path(__file__).with_name("dvr.env")
CHANNELS = (1, 2, 3, 4, 5)  # 6-8 exist on the DVR but have no cameras

# The DVR encodes 1080N: a 1920x1080 image squeezed into 960x1080. Every frame
# has to be stretched back out horizontally or everything looks tall and thin.
NATIVE = (960, 1080)
DISPLAY = (1920, 1080)


def _config():
    cfg = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                cfg[k.strip()] = v.strip()
    for k in ("DVR_HOST", "DVR_PORT", "DVR_USER", "DVR_PASS"):
        if os.environ.get(k):
            cfg[k] = os.environ[k]
    return cfg


CFG = _config()
HOST = CFG.get("DVR_HOST", "")
PORT = CFG.get("DVR_PORT", "554")
USER = CFG.get("DVR_USER", "")
PASS = CFG.get("DVR_PASS", "")


def require_config():
    """Fail loudly rather than half-connect. Nothing identifying the DVR is
    hardcoded here -- it all lives in dvr.env, which is gitignored."""
    missing = [k for k, v in (("DVR_HOST", HOST), ("DVR_USER", USER),
                              ("DVR_PASS", PASS)) if not v]
    if missing:
        raise SystemExit(f"{', '.join(missing)} not set - fill in {ENV_FILE.name}")


def rtsp_url(channel, subtype=0, redact=False):
    """Dahua-style RTSP URL. The password is percent-encoded because it
    contains '@', which would otherwise end the userinfo section early and
    leave a bogus hostname."""
    pw = "***" if redact else quote(PASS, safe="")
    return (f"rtsp://{quote(USER, safe='')}:{pw}@{HOST}:{PORT}"
            f"/cam/realmonitor?channel={channel}&subtype={subtype}")


# Force RTSP over TCP (UDP drops badly on this DVR) and set a socket timeout,
# without which a dead channel blocks read() forever instead of returning False.
# This has to happen before cv2 is imported so the FFmpeg backend picks it up.
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = (
    "rtsp_transport;tcp|timeout;8000000|max_delay;500000")
os.environ.setdefault("OPENCV_LOG_LEVEL", "ERROR")

import cv2  # noqa: E402


class Camera:
    """One camera, read continuously on its own thread.

    Only the newest frame is kept, so a slow consumer drops frames instead of
    backing up a queue, and one dead channel cannot stall the others.
    """

    def __init__(self, channel, subtype=0):
        self.channel = channel
        self.subtype = subtype
        self.status = "stopped"
        self.fps = 0.0
        self._frame = None
        self._lock = threading.Lock()
        self._stop = threading.Event()
        self._thread = None

    def start(self):
        self._stop.clear()
        self._thread = threading.Thread(
            target=self._run, name=f"ch{self.channel}", daemon=True)
        self._thread.start()
        return self

    def stop(self):
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=3)

    def read(self, size=DISPLAY):
        """Newest frame, aspect-corrected to `size`, or None if not connected.
        Pass size=None to get the raw 960x1080 frame."""
        with self._lock:
            frame = None if self._frame is None else self._frame.copy()
        if frame is None or size is None:
            return frame
        interp = cv2.INTER_AREA if size[0] < frame.shape[1] else cv2.INTER_CUBIC
        return cv2.resize(frame, size, interpolation=interp)

    def _run(self):
        backoff = 1
        while not self._stop.is_set():
            cap = cv2.VideoCapture(rtsp_url(self.channel, self.subtype), cv2.CAP_FFMPEG)
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            if not cap.isOpened():
                self.status = "open failed"
                cap.release()
                self._stop.wait(backoff)
                backoff = min(backoff * 2, 15)
                continue

            self.status, backoff = "live", 1
            n, t0 = 0, time.time()
            while not self._stop.is_set():
                ok, frame = cap.read()
                if not ok or frame is None:
                    self.status = "reconnecting"
                    break
                with self._lock:
                    self._frame = frame
                n += 1
                if n % 10 == 0:
                    now = time.time()
                    self.fps, t0 = 10 / (now - t0), now
            cap.release()
        self.status = "stopped"


def tune_encoder(bitrate=2048, fps=25):
    """Push the best settings this XVR will actually hold.

    Hardware limits, established by testing: resolution is fixed at 1080N,
    total budget is 12288 kbps / 120 fps across all 8 channels, and 25 fps
    works on channel 1 only. Channels 6-8 are starved because they have no
    cameras -- their share of the budget is what makes 2048 kbps possible on
    the five that do.
    """
    import re
    import urllib.request as u

    base = f"http://{HOST}"
    mgr = u.HTTPPasswordMgrWithDefaultRealm()
    mgr.add_password(None, base, USER, PASS)
    op = u.build_opener(u.HTTPDigestAuthHandler(mgr), u.HTTPBasicAuthHandler(mgr))

    def get(path):
        return op.open(base + path, timeout=15).read().decode("utf-8", "replace")

    parts = []
    for ch in range(8):
        br, f = (bitrate, fps) if ch < 5 else (320, 1)
        p = f"Encode[{ch}].MainFormat[0].Video"
        parts += [f"{p}.BitRate={br}", f"{p}.FPS={f}", f"{p}.GOP={f}"]
    resp = get("/cgi-bin/configManager.cgi?action=setConfig&" + "&".join(parts))
    print("setConfig ->", resp.strip() or "(empty)")

    # This firmware returns OK for values it then silently discards, so the
    # only way to know what landed is to read the config back.
    cfg = get("/cgi-bin/configManager.cgi?action=getConfig&name=Encode")
    for line in cfg.splitlines():
        m = re.match(r"table\.Encode\[(\d)\]\.MainFormat\[0\]\.Video\.(\w+)=(.*)", line)
        if m and int(m.group(1)) < 5 and m.group(2) in ("BitRate", "FPS", "resolution"):
            print(f"  ch{int(m.group(1)) + 1}  {m.group(2)}={m.group(3)}")


def _tile(cam, size):
    frame = cam.read(size)
    if frame is None:
        frame = np.zeros((size[1], size[0], 3), np.uint8)
        text, colour = f"ch{cam.channel}  {cam.status}", (90, 90, 235)
    else:
        text, colour = f"ch{cam.channel}  {cam.fps:4.1f} fps", (255, 255, 255)
    cv2.rectangle(frame, (0, 0), (size[0], 24), (30, 30, 30), -1)
    cv2.putText(frame, text, (8, 17), cv2.FONT_HERSHEY_SIMPLEX, 0.45, colour, 1,
                cv2.LINE_AA)
    return frame


def _grid(cams, size, cols):
    tiles = [_tile(c, size) for c in cams]
    blank = np.zeros((size[1], size[0], 3), np.uint8)
    while len(tiles) % cols:
        tiles.append(blank)
    return np.vstack([np.hstack(tiles[i:i + cols])
                      for i in range(0, len(tiles), cols)])


def main():
    ap = argparse.ArgumentParser(description="Live view of the DVR cameras.")
    ap.add_argument("-c", "--channels", type=int, nargs="+", default=list(CHANNELS))
    ap.add_argument("-s", "--subtype", type=int, default=0, choices=(0, 1))
    ap.add_argument("--width", type=int, default=480, help="tile width in px")
    ap.add_argument("--cols", type=int, default=3)
    ap.add_argument("--tune", action="store_true", help="re-apply DVR encoder settings")
    args = ap.parse_args()

    require_config()

    if args.tune:
        tune_encoder()
        return

    single = len(args.channels) == 1
    width = 1280 if single else args.width
    size = (width, round(width * DISPLAY[1] / DISPLAY[0]))  # keep 16:9

    cams = [Camera(c, args.subtype).start() for c in args.channels]
    win = f"DVR ch{cams[0].channel}" if single else "DVR"
    print(rtsp_url("N", args.subtype, redact=True))
    print(f"streaming {args.channels} at {size[0]}x{size[1]} per tile - q to quit")
    cv2.namedWindow(win, cv2.WINDOW_NORMAL)

    try:
        while True:
            img = _tile(cams[0], size) if single else _grid(cams, size, args.cols)
            cv2.imshow(win, img)
            key = cv2.waitKey(20) & 0xFF
            if key in (ord("q"), 27):
                break
            if key == ord("s"):
                path = Path(__file__).with_name(f"snap_{int(time.time())}.jpg")
                cv2.imwrite(str(path), img)
                print(f"saved {path.name}")
    finally:
        for cam in cams:
            cam.stop()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
