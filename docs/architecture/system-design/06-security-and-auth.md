# 06. Security, Authentication and Privacy Design

Authentication, authorisation, credential handling, transport security, and
the governance around the one biometric capability IBVAP carries. Sourced from
RFC 0004, RFC 0006, and ADRs 0007, 0008 and 0059.

## Contents

- [Authentication](#authentication)
- [Authorisation](#authorisation)
- [Credential handling](#credential-handling)
- [Transport security](#transport-security)
- [Attribution and audit](#attribution-and-audit)
- [Read-only guarantee against the estate](#read-only-guarantee-against-the-estate)
- [Privacy and biometric governance](#privacy-and-biometric-governance)
- [Egress authenticity](#egress-authenticity)

## Authentication

An opaque session id in an HTTP-only, `SameSite=Strict`, `Secure` cookie, held
server-side; passwords hashed with Argon2id
([ADR 0033](../../adr/0033-backend-framework-packaging-and-auth.md)). No token
leaves the machine and no external identity provider is contacted.

Failed attempts trigger a **progressive, self-clearing delay**, not an
admin-cleared lockout — three distinct sentences distinguish a disabled, an
expired, and a locked account
([ADR 0037](../../adr/0037-sign-in-follows-the-reference-username-password.md)).
Password recovery has two independent paths: an emailed network reset, and a
**local administrator reset** performed on-machine by a second account holding
`can_reset`, with no network required
([ADR 0055](../../adr/0055-offline-password-recovery-by-local-admin-reset.md)).
Every reset is attributed — who, for whom, when.

## Authorisation

One role distinction exists: `can_reset`. Every other authenticated user can
do everything else. This is a deliberate simplification for a one-operator
post, recorded explicitly so a later multi-user site knows exactly which
assumption to revisit rather than discovering it by accident (RFC 0004,
Cross-cutting concerns).

## Credential handling

Recorder credentials are held once per recorder, never per camera, and never
appear in a log line, an API response, or an error message — the URL is
redacted at every boundary the same way the developer rig's own tooling
redacts it. No password column exists anywhere except `users.password_hash`;
recorder and HMAC secrets are indirected through a `secret_ref` column so a
database file copied off the machine for debugging carries no estate
credentials with it (RFC 0001, RFC 0003).

## Transport security

HTTPS with a self-signed certificate generated at install — a site with no
internet has no path to a public CA. The session cookie is `Secure`, which
requires it. The certificate's fingerprint is shown at commissioning so an
operator can recognise their own machine (RFC 0004, Cross-cutting concerns).

## Attribution and audit

Every consequential row — a rule version, an assessment, a mute, a capability
override, a settings change, a password reset — carries the user who caused it
and when, by construction, rather than through a separate audit log that could
fall out of sync with the data it describes. Rule edits create new versions
rather than mutating existing ones; alert assessments are append-only. A
refusal overridden by a named authority is permanently marked on every Event
produced under it ([ADR 0007](../../adr/0007-refuse-unsupported-capabilities-not-degrade.md)).

## Read-only guarantee against the estate

The ingest layer issues only RTSP session opens and ONVIF `Get*` calls. It
contains no code path that writes a device setting, kept true by construction
rather than by discipline — a `Set*` call in this layer is treated as a defect
([ADR 0004](../../adr/0004-function-without-remote-monitoring-layer.md); RFC
0001, Cross-cutting concerns).

## Privacy and biometric governance

**Face detection produces a box and nothing else, unconditionally** — no
embedding, no comparison, no gallery involvement, regardless of whether
recognition is configured anywhere
([ADR 0008](../../adr/0008-face-detection-unconditional-gated-recognition.md)).

**Face recognition is a system-wide switch, not a per-camera or per-rule
one.** It stays refused on every camera until an administrator completes and
enables `watchlist_config` — four conditions: a recorded legal basis, an
authority record (never itself treated as proof the legal basis is valid), a
retention period, and the bounded gallery — plus an explicit `enabled` toggle
that populating the other four does not itself imply
([ADR 0059](../../adr/0059-face-recognition-ships-against-a-configured-watchlist.md)).
Until then, SFace is never loaded and no row is ever written to
`watchlist_matches`.

Where enabled: an embedding is a biometric template, held under the
configured retention clock, never exported. Every match is logged with the
subject, the similarity score, and the threshold in force at the time — and a
match is never acted on automatically. It produces an Event like any other
detection and an Alert only if the matching rule is alerting; an operator
assesses it real, not real, or unsure, exactly as any other alert (RFC 0006,
Cross-cutting concerns).

**No case-management, legal, or governance workflow is built here.** RFC 0006
consumes the `watchlist_config` gate; it does not construct the apparatus
around deciding legal basis or authority, which stays out of scope per
[ADR 0016](../../adr/0016-mvp-ui-cut-to-five-screens.md). This is a real gap —
see [10-risks-and-open-items.md](10-risks-and-open-items.md).

## Egress authenticity

Outbound events to the C2 system are signed HMAC-SHA256 over the raw request
body, verifiable whether or not TLS is available on that network — the
contract should not require a certificate authority no isolated site has. Full
transport detail is in
[07-integration-and-egress.md](07-integration-and-egress.md).
