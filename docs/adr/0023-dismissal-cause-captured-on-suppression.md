# 23. Dismissal cause captured on suppression, not on assessment

**Date:** 2026-08-26
**Status:** Accepted

## Context

[investigative-case-management-platforms.md](https://app.notion.com/p/3c986dda46e281a88c75e6b2d7bf373e?pvs=204)
found alarm-management and SIEM practice converge on capturing a reason at
the consequential act (shelving, suppression, closure), never at first
acknowledgement, using a short closed list with an explicit "undetermined."
This preserves one-tap assessment while still populating a required cause
histogram. No source found publishes a scene-cause taxonomy for video, so
the shipped list is recorded as an unvalidated first attempt.

## Decision

The cause behind a `not real` assessment is captured when a human applies
or reconfirms the per-camera-per-rule mute — never on the one-action
assessment itself. Capture is one optional tap on a short, site-extensible
preset list (e.g. wind, animal, shadow, glare, rain, other, don't know);
never free text, never blocking.

## Consequences

Applies to the mute flow on the current build's Alerts & Events screen —
see [UX.md](https://www.figma.com/design/ZDrrYveQkuzTFD9VufbQZO/IBVAP-%E2%80%94-Product-Design?m=auto&t=crzSM6HZroTo7LFV-6) S-04. The preset list itself remains
unvalidated pending real deployment feedback.
