# 55. Offline password recovery returns, as a local administrator reset

**Date:** 2026-09-03
**Status:** Accepted — settles the regression flagged in [0037](0037-sign-in-follows-the-reference-username-password.md)

## Context

[0024](0024-session-lockout-and-recovery-for-one-person-site.md) designed
recovery for a one-person site with no IT support: pre-issued single-use codes,
plus a local administrator reset, and explicitly no email, no SMS and no security
questions — because none of those work at a Border Out Post with no link.

[0037](0037-sign-in-follows-the-reference-username-password.md) superseded it to
follow the reference design: username and password, optional "remember me", and a
"forgot password" reset. It dropped the post ID, the passphrase and the
pre-issued codes. In doing so it recorded a real regression on itself — recovery
now needs the network — and assigned the question to
[RFC 0004](../rfcs/0004-web-application-and-api-contracts.md).

The constraint has not changed. The site must function correctly with no remote
link for at least 72 hours
([0004](0004-function-without-remote-monitoring-layer.md)). An operator locked
out on day one of a three-day outage, whose only recovery path is an email, is
locked out for three days — and the console is the only way to see what the
cameras are reporting.

## Decision

**A local administrator reset returns, alongside the network reset. Both ship.**

A second account holds a `can_reset` right. That account can set another user's
password from the console, on the machine, with no link — `POST
/api/users/{id}/password`. Every reset records who performed it, for whom, and
when.

The network-based reset stays for sites that do have a link, because it does not
require a second person to be present.

The pre-issued single-use codes from 0024 do **not** return. A printed code in a
drawer at an unstaffed post is not obviously safer than a named colleague who has
to sign in and be recorded doing it, and it adds a commissioning step — generate,
print, distribute, store — to a process the constraints require a non-specialist
to complete in under an hour.

Everything else 0037 settled is unchanged: configurable timeouts, a progressive
self-clearing delay rather than an administrator-cleared lockout, three distinct
sentences for disabled, expired and locked, and a minimum-length-only password
rule.

## Consequences

The offline recovery path exists again, which is the point. A post with two
accounts can recover from a forgotten password with no network and no phone call.

It requires two accounts to exist, which is a commissioning obligation rather
than a feature: a site set up with a single account has no offline recovery, and
the commissioning checklist has to say so. This is a genuine gap for a
truly one-person post, and it is accepted because the alternative — a printed
code that must be generated, stored somewhere findable, and kept out of the wrong
hands — has failure modes that are worse and harder to notice.

It introduces the one role distinction the platform has.
[0016](0016-mvp-ui-cut-to-five-screens.md) cut the people-and-roles screen, so
`can_reset` is set at commissioning and not editable in the console. That is a
deliberate simplification for a one-operator post, and a later multi-user site
will need to revisit it — which is worth knowing now rather than discovering.

The reset is a consequential action and is attributable, like every other one. An
administrator who resets a colleague's password leaves a record; there is no path
by which someone's password changes without the change being traceable to a
person.

The progressive self-clearing lockout from 0024 remains the first line of
defence, and it matters more given this decision: most lockouts should clear
themselves within minutes, and the administrator reset is for a genuinely
forgotten password rather than for a mistyped one.
