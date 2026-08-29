# 30. Dark console palette — colour marks category and attention, never severity

**Date:** 2026-08-29
**Status:** Accepted

## Context

Until now the only recorded commitment about IBVAP's visual language was
"dark-first, Night default," carried as a line in
[CLAUDE.md](../../CLAUDE.md) §4 rather than as a decision. A UI kit had in
fact been built in the
[Figma design file](https://www.figma.com/design/ZDrrYveQkuzTFD9VufbQZO/IBVAP-%E2%80%94-Product-Design)
— token collections, a type ramp, and roughly two dozen components — but
the reasoning behind its colours lived only on a board inside that file.
That left the most easily-violated part of the design unrecorded, and
colour is the part most likely to be undone by whoever builds the next
screen, because the conventional operational grammar is so strong.

That grammar — red for bad, amber for warning, green for good — is exactly
what this product may not use. IBVAP computes no threat score and assigns
no severity: [0018](0018-operator-assigned-impact-grade.md) makes an impact
grade the assessor's own judgement and never a system finding, and
[0016](0016-mvp-ui-cut-to-five-screens.md) leaves alert-versus-logged as
the only distinction the system itself draws. A red alert badge would
silently reintroduce a severity tier the product refuses to compute. The
same applies to refusal: under
[0007](0007-refuse-unsupported-capabilities-not-degrade.md) a camera that
cannot support a class is a correct, honest outcome, so colouring it like
a fault would misreport a success.

Reviewed on 2026-08-29, the palette as first built was also too
high-chroma to be instrumental — saturated magenta, spring green and sky
blue read as decoration on a screen whose job is to be watched at night at
a border post.

## Decision

Night is the default mode and Day is a second mode on the same theme
collection, so nothing is defined twice. Tokens are two-layer: a primitive
ramp holding raw values, and a semantic theme layer aliasing it.
Components bind only to the semantic layer.

The neutrals are a low-chroma cool slate, and separation between surfaces
is carried by hairline borders and value rather than by shadow or by
rounding. Interface type is Inter; anything a person may have to read out,
copy or compare — stream addresses, plate reads, timestamps, event ids,
payloads — is JetBrains Mono.

Three rules govern colour, and they are encoded in the tokens rather than
left to each screen:

1. **Nothing in the chrome uses colour to mean good or bad** — no green for
   pass, no red for fail. A single attention colour, a burnt amber, carries
   the annunciator sense of "a human should look at this." Alert versus
   logged is a binary, never a scale.
2. **A refused capability is informational blue, not an error colour**, and
   must never be mistaken for a fault.
3. **The real / not real / unsure triad is colourless.** The three are
   peers; giving any of them a hue would rank them, and an assessment is a
   fact recorded rather than a judgement scored.

Detection overlays are the one place hue is categorical. The four classes
sit at deliberately equal lightness with spread hue, so they read as four
kinds of thing rather than four degrees of one thing, and their hues are
adapted from a colour-vision-deficiency-safe set. They have to stay legible
on both a bright daylight frame and a monochrome IR frame, because the same
camera produces both.

The token values themselves live in Figma and are not restated here, per
[CLAUDE.md](../../CLAUDE.md) rule 5.

## Consequences

A raw colour value inside a component is a defect, not a shortcut — every
fill, stroke and text colour resolves through the semantic layer, which is
what allowed the whole kit to be re-toned by editing primitives alone.
Adding or correcting a Day-mode value is an edit to the theme collection
and never a change to a component.

The three rules are enforceable at review: introducing a red or green
status colour, or giving one of the assessment options a hue, is a change
to this decision and needs a superseding ADR, not a styling call on a pull
request.

Two defects surfaced while applying this and were fixed: the muted text
token resolved to the same primitive in both modes and failed WCAG AA
against the Night canvas, so it is now set per mode; and a pill radius
token existed with no bindings, which would have invited rounded chrome
this palette does not use.

[CLAUDE.md](../../CLAUDE.md) §4 is updated — the UI kit is no longer listed
as unbuilt, and what remains open is the missing components and the
still-empty hi-fi page. Wireframe review, RFC 0001 and the outstanding RFCs
are untouched by this decision.
