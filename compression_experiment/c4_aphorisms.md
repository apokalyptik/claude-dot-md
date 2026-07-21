# CLAUDE.md — Maxims (law: PHILOSOPHY.md)

Demands on ourselves; never on others.
Selfish code: easier to write, harder to understand. Correct is not a defense.
Judge everything by the reader: grep and vim at 3am, no IDE, one pass, no leaving their place.
Rules are case law; the principle decides what they don't. Never obey a rule in a way that burdens the reader.
Critique code, never its author.

Guards discharge; accumulators decide. Two levels deep — a pattern is missing.
Guards own rejection; defaults stay innocent.
A screen of work; two with a reason; past that, stop and ask.
Simple check-and-exit is free; setup is work wherever it sits.

Say the name in a sentence, or rename it. Abbreviation is theft from the reader.
If grep can't find it, it's lost. Name as if the namespace weren't there.

Statements, not expressions — the reader never decompiles.
No ternaries. Coalesce defaults in the open, never buried.
Switch, not match: evaluation may assign; match must. Break every case; default every switch.
One operator between two conditions; more than that, name the pieces.
foreach, not array_map. Extra obvious lines are the price, gladly paid.

Extract when divergence would be a bug, or when a name can tell the whole truth.
Coincidental twins stay apart. Short functions are a symptom, not a goal.
A function is as long as its one nameable idea.
A name is a contract for life. Behavior changed? Rename or new function — and with many callers, the user decides on the evidence.

Write cut, grep, sort — not awk.
Take the card, the amount, the currency — never the Invoice that carries them.
Domain objects live at the boundary; building blocks never meet them. The god class is the collapse.

Errors return; they do not throw. A throw taxes every layer forever.
Document the sentinel; check it on the very next line; never let it collide with success.
Foreign throws die at the border, converted.
Validate everything, even the input you trust.

Comments narrate why; the code itself is the what.
Sequester what must be complex into the smallest possible room.

This document beats the neighborhood: copy conventions, never violations. Prevalence is not permission.
Touch only what you author; unwind only what you land in; never fix what you weren't asked to.

Five stops, always with evidence, always waiting:
tempted by a banned form — show both versions;
the plain version sprawls — prove it in written code;
past two screens — weigh the split;
many callers, changed behavior — list them, assess them, let the user choose;
a failing test — never silence it; regression or renegotiation, the human rules.
Approvals live once; only this document makes them law.

Test promises, not accidents: if it could change with every promise kept, don't assert it.
A flaky suite breeds blindness. Tests stand alone; their repetition is a virtue; their names run long.
Prove the guards: valid in, invalid in, both asserted.
