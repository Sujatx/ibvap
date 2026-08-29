# 31. Component grammar — a chip states a fact, a segmented control makes a choice

**Date:** 2026-08-29
**Status:** Accepted

## Context

[0030](0030-dark-console-palette-no-severity-colour.md) settled colour but
said nothing about form, and building out the components the five screens
need forced a question the wireframes had left open: the same interaction
was drawn two different ways.

Three places on `01 Wireframes` ask the operator to pick exactly one option
from a small closed set — draw mode (line / zone / select) on S-03, what a
rule does when it fires (raise an alert / log only) on S-03, and transport
(webhook / REST / MQTT) on S-05. All three are drawn as loose chips. But
the assessment control on S-04 asks exactly the same kind of question —
real / not real / unsure — and is drawn as three adjacent bordered boxes
with the chosen one inverted. Two grammars, one interaction.

Chips were also doing double duty. The `Chip` component's own description
in the Figma kit already said it is "a small standing fact — a state, a
filter, a detected class. Never a button," which the wireframes then
contradicted three times. A control an operator is expected to press
should not look identical to a label reporting that it is night.

The same build surfaced a second, narrower question. Detection overlay
labels sit on a class colour that is deliberately identical in Night and
Day, so a fixed dark label text works in both. Rule geometry is not like
that: an operator-drawn line or zone is white at night and near-black by
day. Copying the detection label treatment onto rule geometry produced
dark text on a dark ground in Day mode — unreadable, and caught only
because both modes were rendered.

## Decision

**An exclusive choice is a segmented control.** Adjacent bordered boxes,
equal weight, the chosen one inverted — the grammar the assessment control
already used. Selection is carried by inversion and never by a hue, which
keeps it inside [0030](0030-dark-console-palette-no-severity-colour.md)'s
third rule: options in a set are peers, and colouring one would rank them.

**A chip states a fact and is never a control.** A state the console is
already in, a class that was detected, a filter that is currently applied.
If pressing it changes something, it is not a chip.

Sizes come from the token scale, not from the wireframes. The wireframes
carry eyeballed control heights; the small and medium control tokens are
what the components use, and where the two disagree the token wins.

**Chrome drawn over video takes a foreground that inverts with its
ground.** Where a background token holds the same value in both modes, its
foreground may be fixed; where the background inverts — as operator-drawn
rule geometry does — the foreground must invert with it. This is a
property of the token pair, checkable when the component is built rather
than discovered on a screen.

## Consequences

The three wireframe spots that drew chips as pickers will look different
once they are built, and that is the point: an operator can now tell by
shape alone whether something is reporting or asking. The `Chip`
description becomes true rather than aspirational.

Every component binds only to the semantic theme and dimension layers, and
this is now checked rather than trusted — a sweep for raw fills, strokes,
spacing, radii and stroke weights, for anything bound to the primitive
ramp, and for unstyled text, is part of finishing a component. The sweep
across the fifteen components built under this decision returned nothing,
and confirmed no new variable, style or collection had been introduced.

Rendering both modes is part of finishing a component too. The Day-mode
label defect described above was invisible in Night and would have shipped.

Three components predate the generics this decision produced and duplicate
them — the payload preview holds its own code block, the mute duration
menu its own popover shell, and the alert detail its own hand-built record
list. They are deliberately left alone rather than reworked; the
duplication is known, is not a correctness problem, and rebuilding
reviewed components is not worth delaying the first full-fidelity screen.

The component gap listed in [CLAUDE.md](../../CLAUDE.md) §4 is closed.
Drawing S-02 Live View at full fidelity is now unblocked; wireframe review,
RFC 0001 and the outstanding RFCs are untouched by this decision.
