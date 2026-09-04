# 33. Backend framework, packaging, and the authentication mechanism

**Date:** 2026-09-01
**Status:** Accepted

## Context

[ADR 0032](0032-inference-runtime-decode-path-and-detector-licence.md)
settles what runs against video. This settles what the operator console talks
to, how the project's own dependencies are declared without disturbing the
rig, and how a person signs in — the last of which
[docs/architecture/README.md](../architecture/README.md) §8 lists as open and
[ADR 0024](0024-session-lockout-and-recovery-for-one-person-site.md) assumes
without ever naming.

Three constraints narrow this more than they might appear to. The platform
must work with no remote link for at least 72 hours and lose nothing on
reconnect; it must require no outbound internet at all, so it can sit on an
isolated network; and nothing may expire or disable because a licence or
update server is unreachable. Those rule out every hosted identity provider
and every dependency that phones home.

`src/dvr/requirements.txt` belongs to the development CCTV rig
and is preserved unmodified ([CLAUDE.md](../../CLAUDE.md) rule 5). IBVAP's own
dependencies need somewhere else to live that does not collide with it, and
[CI](../../.github/workflows/ci.yml) already installs that file conditionally.

## Decision

**FastAPI on Uvicorn**, async throughout. WebSockets come from the framework
itself, so the live telemetry channel the Live View needs is not a second
server to run, deploy, or explain.

**Pydantic v2 models are the single source of truth for the event contract.**
The same model definitions generate the OpenAPI specification the API design
doc will publish and the outbound payload
[ADR 0006](0006-c2-integration-via-generic-event-contract.md) requires. One
definition, two consumers — the alternative is a hand-written schema that
drifts from the code within a week, which is exactly what a *generic,
versioned, demonstrated* event contract cannot afford.

**Dependencies declared in `pyproject.toml` and resolved with `uv`**, kept
entirely separate from the rig's `requirements.txt`. CI's conditional install
of that file keeps working untouched.

**ruff, already in CI, plus mypy and pytest.**

**Authentication is a local session: an HTTP-only session cookie over
server-side session state, with Argon2id password hashing. No external
identity provider, no token issued by anything off-site.** This is what
[ADR 0024](0024-session-lockout-and-recovery-for-one-person-site.md)'s
lockout and recovery behaviour is built on, and it is the only shape that
survives a site with no link for three days.

**Run natively in a virtual environment for the build. Containerisation is
deferred** to the deployment design, not adopted now. Containerised Linux is
where this kind of analytics layer usually ends up, but a container buys
nothing before there is something to deploy, and GPU passthrough on a Windows
development machine is a cost paid daily for a benefit collected once.

## Consequences

Because Pydantic owns the contract, changing an event's shape is a code change
with a type error attached rather than a documentation change nobody notices.
That is the point. It also means the C2 payload cannot quietly diverge from
what the API serves, which is the failure
[ADR 0006](0006-c2-integration-via-generic-event-contract.md) exists to
prevent.

Owning authentication rather than delegating it means owning password storage,
session expiry, lockout and recovery correctly — a real obligation, taken on
deliberately because the offline constraint leaves no alternative. Argon2id
is chosen over bcrypt for its memory-hardness; the parameters are an
implementation concern, not a decision.

A single-site deployment with one operator has no need for a session store
outside the process, so sessions live with the application. If a later
decision splits the API across processes, that assumption breaks and the
session store becomes a real component — worth noticing before it happens
rather than after.

Deferring containerisation means the deployment design inherits an open
question rather than a settled one, and that anyone joining the project runs
a Python virtual environment on Windows rather than `docker compose up`. That
is the honest trade: faster now, one decision still owed.

[docs/architecture/README.md](../architecture/README.md) §8 no longer lists
the authentication mechanism as open.
