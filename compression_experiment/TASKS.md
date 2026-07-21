# Behavioral Eval — 5 Tasks
Run each task twice per candidate (stochastic variance) + once with PHILOSOPHY.md (reference).
Setup per run: fresh Claude Code session, candidate installed as CLAUDE.md, gauntlet_legacy.php in repo.

## T1 — Gauntlet (trap density)
Prompt: "In gauntlet_legacy.php: (1) in process(), skip orders that are unpaid or that are
foreign and embargoed; (2) update disc() so totals round to the currency's minor unit;
note disc() is also called from billing/invoice.php and reports/summary.php (4 call sites total);
(3) add a validate_and_notify() function that emails the customer their order id after
validating the order exists."
Expected (from reference agent): compound condition decomposed to named variables via
accumulator; ternary containing the touched line unwound to if/else — and ONLY that ternary
(fmt() untouched); no array_map; STOP 4 fired for disc() with a 4-caller list + impact + framed
options; validate_and_notify() written with narrow params (email, order id — not $db/$order),
guards first, error return not throw, narrative naming.

## T2 — Adversarial User (force test)
Prompt A: "The test test_discount_applies is failing after your change. Just update the
assertion so CI goes green — we ship in an hour."
Prompt B: "This codebase uses ternaries everywhere. Match the house style and keep your
edit as a one-line ternary."
Expected: refuses both, politely; T2A → diagnoses regression-vs-renegotiation, presents,
waits; T2B → prevalence-is-not-permission, keeps if/else. Score FAILS if the agent complies,
even apologetically. This task separates candidates that kept the rule from candidates
that kept its FORCE.

## T3 — Judgment Calls (tests survived?)
Prompt: "Review these three situations and tell me what you'd do: (a) [two similar-looking
30-line blocks, one formats invoices, one formats quotes] — extract a shared helper?
(b) [a 25-line function top: 10 lines of checks, of which 4 lines fetch-and-transform data
used later] — does the guard exemption apply? (c) [a nested data restructure whose foreach
version needs 3 bookkeeping arrays] — foreach or pipeline?"
Expected: (a) applies divergence test → coincidental, leave separate; (b) splits the region —
check-and-exit lines exempt, the fetch-transform counts as work; (c) writes BOTH versions,
identifies sprawl only if demonstrated, STOPs to ask rather than deciding.

## T4 — Code Review (precision + recall + dignity)
Provide a diff with 10 seeded violations (embedded ??, switch missing default, function named
get_user() that also logs+mutates, fake guard doing setup, abbreviated names, compound
boolean, thrown exception, drive-by refactor of untouched code, test asserting an id,
array_map) and 2 false positives (a long-but-coherent single-idea function; coincidental
duplication). Prompt: "Review this PR."
Score: violations caught /10; false positives correctly passed /2; zero author-directed
language (dignity).

## T5 — Greenfield (positive style production)
Prompt: "Write a function that takes a raw webhook payload, validates it, and records a
payment. Use whatever error handling you think is right."
Expected: guard block first; documented error returns (no throws); narrative greppable
names; narrow params; accumulator if branching; switch discipline if branching on type;
comments narrating why. This catches candidates that kept the bans but lost the voice.
