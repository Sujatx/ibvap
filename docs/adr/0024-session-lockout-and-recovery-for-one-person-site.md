# 24. Session, lockout and recovery for a one-person, no-IT site

**Date:** 2026-08-26
**Status:** Accepted

## Context

[investigative-case-management-platforms.md](../01-research/competitors/investigative-case-management-platforms.md)
found the governing standards (NIST SP 800-63B, CJIS Security Policy)
genuinely disagree on timeout numbers by design, that the standard lockout
mechanism assumes an administrator a single-operator post doesn't have,
and that both standards explicitly forbid security questions and stored
hints — while email/SMS recovery is independently ruled out for this
deployment context. The research also found a standing, citable exemption
for receive-only terminals that remain staffed.

## Decision

Session timeouts are configurable, never hard-coded. Failed sign-in
triggers progressive delay rather than an administrator-cleared lockout;
any lockout is self-clearing after a stated, on-screen interval. Recovery
is a pre-issued, single-use recovery code plus a locally held
administrative reset — never a security question, a hint, or an email/SMS
round-trip. No password expiry or composition rule beyond a stated minimum
length. Disabled, expired and locked are three distinct states with three
distinct sentences.

## Consequences

See [UX.md](../03-design/UX.md) S-01 (Sign in).
