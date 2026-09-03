# 56. An event carries exactly one primary class

**Date:** 2026-09-03
**Status:** Accepted — settles the store obligation named in [0046](0046-timeline-markers-carry-class-colour.md)

## Context

[0046](0046-timeline-markers-carry-class-colour.md) reversed the earlier rule
that timeline markers carry no hue: a marker's colour now names the detection
class, using the same four `DetectionBox` tokens, while its weight still names
alert versus logged. It closed by noting that this creates an obligation on the
store — every marker now needs a class — and that the event-store RFC has to
decide what a mixed or classless event gets.

The cases are real. A rule can filter on more than one class. A rule can be
satisfied by two tracks of different classes in the same zone on the same frame.
And a movement-based rule fires on a MOG2 region that no classifier has looked
at.

The tempting answer is a fifth, neutral marker colour for "mixed". It is tempting
because it is honest about the ambiguity. It is wrong because
[0030](0030-dark-console-palette-no-severity-colour.md) fixes the palette at four
detection colours chosen for equal lightness and CVD-safe hue spread, and a fifth
token invented for an edge case would be the one colour in the system that means
"several things" rather than "a thing".

## Decision

**An Event stores exactly one `primary_class`: the class of the
highest-confidence track that satisfied the rule. A separate boolean
`class_mixed` records that other classes were also present, and is not drawn.**

`primary_class` is always one of `person`, `vehicle`, `face`, `plate` — the four
tokens 0046 draws with. `class_mixed` is available to a detail panel, which can
say "a vehicle was also present" in words, where a nuance like that belongs.

A movement-only event with no class cannot occur. A movement primitive is always
evaluated against a rule's class filter, and the rule's declared class is what
the event records — so
[0053](0053-night-movement-as-a-detector-independent-primitive.md)'s
detector-independent movement signal still produces a classed event.

## Consequences

The four-colour marker rule stays total. Every marker resolves, no marker needs a
colour that does not exist, and the palette 0030 defined is unchanged.

"Highest-confidence track that satisfied the rule" is a rule, not a heuristic,
and the determinism matters: the same event replayed produces the same colour on
the timeline. A tie-break by confidence alone could still be ambiguous at equal
confidence, so the implementation breaks ties by track id, which is arbitrary but
stable.

Some information is lost from the marker, deliberately. A timeline showing a
person-coloured marker for an event where a person and a vehicle were both
present is telling a simplified truth. The full truth is one click away in the
detail panel, and the alternative — encoding multiplicity in the axis — would
make a dense day's timeline unreadable to communicate something an operator
rarely needs at that zoom level.

`class_mixed` is stored and not drawn, which means it costs a column and buys a
sentence. That is the right shape: the store records what happened, and the
drawing surface decides what is worth drawing.

The outbound C2 payload carries both fields
([RFC 0005](../rfcs/0005-c2-event-egress-publisher.md)), so a downstream consumer
that does care about multiplicity is not limited by a choice made for a timeline
axis.
