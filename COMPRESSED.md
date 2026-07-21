# CLAUDE.md (derivations: PHILOSOPHY.md)

ROOT (decides everything unlisted): **demands on ourselves, never on others.** Selfish code = easier to write, harder to understand — bad even when tested and correct; "works" is never a defense. Rules below are case law, illustrative not exhaustive, never invertible. The reader gets plain text, grep, vim, one pass, 3am — never their IDE, working memory, mental decompiling, or a trip elsewhere; never tax callers above. Critique code, never authors. PHP/WordPress, long-lived.

FLOW → guards first: early return per terminal condition, as soon as knowable — each discharges a case. Work continues? Accumulator: default + flat ifs + branch on result; guards own rejection (new cases extend guards, never defaults). Two nesting levels = a missing pattern. Length: one screen of working code; two with a reason (one idea extraction can't honestly compress — "it grew" isn't); simple check-and-exit guards exempt, setup counts as work anywhere.

NAMES → full words, never abbreviated, sentence-readable aloud, globally greppable: my_feature_process(), never process(). Namespaces only for collision defense, symbols named as if the namespace were absent.

CONSTRUCTS → statements, not expressions: control flow never hides in an assignment (the test for anything unlisted). No ternaries (appeal = STOP 1). ?? only as a bare visible default assignment ($x = $in ?? 0); embedded → hoist. Switch, not match — evaluation with optional assignment beats forced assignment — and over exclusive if-chains: every case explicitly break/returns, every switch has a default arm reporting failure; positive/negative checks where clearer. Compound booleans banned in both forms (if( $a || $b && !($c||$d) ) and $x = $a || $b): decompose to named variables; one pair/one operator fine, mixed/nested/negated → decompose. foreach, not array_map; extra obvious lines are the intended price.

EXTRACTION → exactly two reasons. (1) Divergence between call sites would be a bug → centralize; otherwise coincidental — leave it. (2) The name is the whole truth (no hidden state, logging, mutation) and readers skip the body. Never for length, lookalikes, or shredding a narrative; short is a symptom, not a goal; a function is as long as its one nameable idea. A name is a lifetime contract: behavior changed and zero other callers → rename freely; multiple callers → STOP 4.

COMPOSABILITY → cut/grep/sort, not awk. Params = narrowest true dependencies (card, amount, currency — never the Invoice carrying them). Domain objects only at orchestration boundaries (guard → decompose → compose); building blocks ignorant of them; god class = the anti-pattern. Params growing → split, or a small grouping of exactly what's used.

FAILURE → errors are documented return values ("returns X, or null on error"; WP_Error where native; compound returns for detail) — never throws: a throw taxes every layer above forever (STOP 1, very high bar). Check fallible returns immediately and adjacently; sentinels never collide with success. Third-party throws: catch at the boundary, convert. Validate all input, even trusted; design against misuse.

COMMENTS → narrate why; code shows what; junior-opaque density gets what-comments; sequester complexity into the smallest self-contained function.

AUTHORSHIP → this document beats house style: mimic conventions, never banned constructs; prevalence ≠ permission; compliant-but-different code is correct — never "fix" it back. New functions comply fully; edits upgrade touched lines only, unwinding just the minimal enclosing violation, cascading no further; no drive-by refactoring without asking.

FIVE FULL STOPS — halt, present evidence, wait for the human:
1. Banned pattern seems necessary or genuinely more readable → BOTH versions as short examples. Nothing downstream of the dispute proceeds (independent work may). Rulings bind one instance — never precedent; permanence only by amending this document. Habit, brevity, "idiomatic" earn compliant code, not a question.
2. Compliant non-functional version sprawls → both versions; sprawl demonstrated in written code, never predicted.
3. Working code past two screens → weigh extraction deliberately; length alone never splits.
4. Multi-caller behavior change → grep-derived caller list, per-site impact assessment, rename-vs-new-function framed; the user decides on evidence, not verdicts.
5. Failing test → NEVER edit it to pass. Regression (fix the code) or contract renegotiation (the human decides). Diagnose, present, wait.

TESTS → assert the essential, never the incidental: could it change with every promise kept? Then don't assert it (title/body/author, never the auto-increment id). Stable suites; false alarms breed smell blindness. Independent by design: repetition between tests fine, names run long, thoroughness beats brevity. Test positive, negative, and invalid input — prove the guards hold.
