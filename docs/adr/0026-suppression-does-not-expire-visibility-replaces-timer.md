# 26. Suppression does not expire; visibility replaces the timer

**Date:** 2026-08-26
**Status:** Superseded by [0027](0027-suppression-works-like-notification-snooze.md)

## Context

Resolves the flag raised in [0025](0025-suppression-auto-expiry-flagged-for-elevation.md):
whether suppression should auto-expire at all. Removing the timer avoids
inventing a product-side duration this project had no basis for, relying
instead on persistent visibility as the safeguard against one accumulating
unnoticed.

## Decision

A suppression stays active until a human reverses it, with no
auto-expiry — persistent visibility (on every screen that shows
suppression state) is the sole safeguard against one accumulating
unnoticed.

## Consequences

Superseded before implementation by
[0027](0027-suppression-works-like-notification-snooze.md), which restores
a timer but makes its duration an operator choice rather than a
product-picked number.
