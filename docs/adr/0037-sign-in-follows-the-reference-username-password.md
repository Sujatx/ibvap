# 37. Sign in follows the reference — username and password, with a password reset

**Date:** 2026-09-01
**Status:** Accepted. Supersedes [0024](0024-session-lockout-and-recovery-for-one-person-site.md)

## Context

[0024](0024-session-lockout-and-recovery-for-one-person-site.md) designed
sign-in around a single-person post that may be offline for days: a post ID
and a passphrase, progressive delay instead of an administrator-cleared
lockout, and recovery by a pre-issued single-use code plus a local
administrative reset. It ruled out security questions, hints, and any
email or SMS round-trip, because a recovery path that needs the network is
no recovery path at a BOP.

The reference design supplied for the Phase 2 wireframe rebuild used a
conventional workstation sign-in instead — username, password, "remember
me", "forgot password", SSO. The conflict was raised when the rebuild was
planned and again when it was delivered. The instruction both times was to
draw the reference exactly. SSO and the theme switcher were then removed on
a follow-up instruction; username, password, remember-me and the password
reset stayed.

That leaves a decision actually made, and 0024 describing a screen that no
longer exists. Recording it is not a rubber stamp: the offline-recovery
reasoning in 0024 was sound, and what replaces it has a real gap that
belongs in the record rather than in a reviewer's memory.

## Decision

Sign-in is username and password, with an optional "remember me" that holds
the username only, and a "forgot password" reset. This is what
`01 Wireframes` draws across all sixteen S-01 frames.

What 0024 established and this decision keeps: session timeouts are
configurable rather than hard-coded; failed attempts produce a progressive,
self-clearing delay rather than a lockout an administrator has to clear;
disabled, expired and locked remain three distinct states with three
distinct sentences; and there is no composition rule beyond a stated
minimum length.

What 0024 established and this decision drops: the post ID, the passphrase,
and pre-issued single-use recovery codes.

SSO is not part of the product. It was drawn from the reference and removed.

## Consequences

**Recovery now depends on the network, and that is a real regression.** A
password reset is a round-trip 0024 rejected on the grounds that this post
can be offline for days. Nothing in the wireframes resolves it — the
`forgot password` frame shows the reset being requested and says nothing
about what happens when the link is down. Either a local administrative
reset comes back alongside the emailed one, or the product accepts that a
forgotten password at a disconnected post is unrecoverable until the link
returns. That choice is not made here and is the first thing RFC 0004
(web application and API contracts) has to settle.

The honest-copy work in the superseded frames is lost with them — the
sentences explaining why there is no security question, no hint and no
email round-trip described a design that no longer ships.

[0024](0024-session-lockout-and-recovery-for-one-person-site.md) is marked
superseded. [0036](0036-wireframe-breakpoints-and-required-state-set.md) is
corrected: it had listed the reference's sign-in among the things the
rebuild refused, which stopped being true when the reference was adopted.
