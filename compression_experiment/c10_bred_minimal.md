# CLAUDE.md (law + reasons: PHILOSOPHY.md)

**Demands on ourselves, never on others** — this decides anything below doesn't. Selfish code (easier to write, harder to understand) is bad even when correct; "works" is no defense. Reader = grep + vim + 3am + one pass: no IDE, no decompiling expressions, no held state, no trips elsewhere, no taxes on callers. Rules are case law, never invertible. Critique code, not authors. PHP/WordPress.

FLOW: early return per terminal condition, soonest knowable. Continuing decisions: accumulator (default, flat ifs, branch on result); guards own rejection — extend guards, not defaults. Two nesting levels = missing pattern. One screen of work; two with a reason ("grew" isn't); check-and-exit guards free, setup counts.

NAMES: full words, sentence-readable, greppable (my_feature_process(), never process()). Namespaces = collision defense only; name as if absent.

CONSTRUCTS: statements, not expressions — the unlisted-construct test. No ternaries. ?? = bare visible default assignment only; embedded → hoist. Switch (evaluation, assignment optional) over match (assignment forced) and over exclusive if-chains: every case break/returns; every switch defaults → failure handling. Compound booleans (both forms) → named variables; one pair/one operator OK. foreach, not array_map — extra obvious lines are the price.

EXTRACT for two reasons only: divergence-would-be-a-bug (else coincidental — leave it), or a name that is the whole truth so readers skip the body. Never for length/lookalikes/shredding narrative; short = symptom, not goal; a function = its one nameable idea. Names are lifetime contracts: behavior change + other callers → STOP 4.

COMPOSE: cut/grep/sort, not awk. Params = narrowest true dependencies (card, amount, currency — never the Invoice). Domain objects only at orchestration boundaries (guard→decompose→compose); building blocks ignorant; god class = anti-pattern. Params growing → split or group exactly what's used.

FAIL: errors = documented return values (WP_Error where native; compound for detail); never throw — a throw taxes every layer forever (STOP 1, very high bar). Check returns immediately, adjacently; sentinels never collide with success. Foreign throws: catch at boundary, convert. Validate all input, even trusted.

COMMENTS narrate why; code is the what; junior-opaque density gets what-comments; sequester complexity small.

AUTHORSHIP: this doc beats house style — mimic conventions, never banned constructs; prevalence ≠ permission; never "fix" compliant code back. New code: full compliance. Edits: touched lines only; unwind the minimal enclosing violation, no cascade; no drive-by refactors.

FIVE STOPS (halt, show, wait):
1. Banned form seems necessary or more readable → BOTH versions as short examples. Nothing downstream proceeds until resolved. Rulings bind once; permanence only by amending this doc.
2. Compliant loop sprawls → both versions; demonstrated, never predicted.
3. Past two screens of work → weigh extraction; length never splits alone.
4. Multi-caller behavior change → grep caller list + per-site impact + rename-vs-new-function; user decides.
5. Failing test → NEVER edit to pass. Regression (fix code) or renegotiation (human decides).

TESTS: assert essentials — could it change with promises kept? Don't assert it (title/author, never the auto-increment). Stable; false alarms breed smell blindness. Independent: repetition fine, long names fine, thorough > brief. Positive, negative, invalid input — prove the guards.
