# When Writing The Code

Full reasoning behind every rule: see PHILOSOPHY.md. When a situation no rule below settles, the governing principle settles it:

**We place demands upon ourselves and do not place demands on others.** The writer absorbs cost — in effort, length, and time — so that readers, callers, debuggers, and maintainers don't. Code made easier to write by means that make it harder to understand is *selfish code*, and it is bad even when tested, functional, and correct. "It works" is never a defense.

The banned constructs below are case law, not statute. The list is illustrative, never exhaustive: judge unlisted constructs by the demands they place downstream — on the reader's tools (code must be fully navigable as plain text with grep and a basic editor; never depend on an IDE), on mental compilation, on working memory, on context switching, on the skill of an exhausted operator in vim at 3am, on debuggers needing observable intermediate state, and on callers building above. Never follow a rule in a way that increases those demands — that inverts the principle the rule serves.

Context: long-lived PHP, WordPress-adjacent codebases read for years by people who didn't write them.

## Structure and Flow

Code is prose meant to be read out loud; read aloud, it should narrate what it is doing. Comments are narration ("First we sanitize the input") and explain *why*; the code itself must explain *what*. Names encode intent. If a junior developer couldn't understand a dense passage by reading it, comments must also explain what it does.

- **Early returns** for conditions that end the function's work. Place them as early as the condition can be known — ideally at the top; mid-function terminal returns are fine when the condition can't be known sooner. Each guard permanently discharges a case from the reader's mind.
- **Accumulator pattern** when a decision is made but work continues: set a variable to a default, adjust it with flat, independent if statements, branch on the result. The default need not be defensive — guards upstream own rejection. New input cases extend the guards, never lean on the default.
- **Tripwire:** two levels deep in conditionals means one of these two patterns is missing.
- **Function length:** one screen of working code is the target; two is acceptable with a reason; beyond two, STOP and deliberately consider extraction — length never forces a split, but always forces the question. The guard block is exempt from all counts, but only true guards: simple, concise check-and-exit lines. Anything that builds toward the result is working code wherever it sits, and complexity in the guard region counts.

## Naming

- **Never abbreviate.** Names must make sense read aloud as part of a sentence.
- **Names must be greppable:** globally unique, fully descriptive. `my_feature_name_process()`, never `process()`.
- **Namespaces** only when defensively necessary (collision protection in shared runtimes, e.g. WordPress plugins) or structurally required. Even then, name symbols as if the namespace did not exist — grep doesn't read namespaces.

## Constructs

**Control flow belongs in statements, not expressions.** Anything that folds branching into an assignment forces the reader to mentally decompile it. Use `if`, `switch`, `foreach`. This is the test for constructs not listed here.

- **Ternaries:** never.
- **Null coalescing:** only as the top-level operation of a simple default assignment — `$limit = $input ?? 10;`. Never embedded inside a larger expression (argument list, condition, concatenation, return). If `??` isn't the first thing the line is obviously doing, hoist it into its own named assignment.
- **Switch, not match.** Every case ends in an explicit `break` or `return` — fallthrough never, even intentionally. Every switch has a `default` arm, even for "impossible" values; it reports failure per Failure Handling. Use switch instead of multiple exclusive ifs on the same variable.
- **Compound conditions:** never combine conditions into a dense boolean like `if ( $a || $b && ! ( $c || $d ) )` — unreadable without precedence knowledge, and undebuggable (no observable intermediate state). Extract each condition into a well-named variable; combine with the accumulator or sequential ifs. One pair of conditions with one operator is fine; mixed operators, nested groups, or negated groups mean decompose. Use multiple if statements instead of one if checking many things.
- **Functional programming:** default to statement form — `foreach`, not `array_map`; a few extra obvious lines is the intended price, not negotiable line-by-line. If avoiding it produces genuine sprawl (scaffolding that buries the logic), that is a readability inversion: STOP and ask. Sprawl must be demonstrated by written compliant code, never predicted.

## Extraction and DRY

Duplication is not inherently bad; extraction is not inherently good. Extract for exactly two reasons:

1. **Consistency** — call sites that *must* agree (authorization checks, validation, sanitization). Test: **if these call sites quietly diverged, would that be a bug?** If not, the duplication is coincidental — leave it alone. Never DRY a simple foreach into a shared map; that's a map by another name.
2. **Cognitive compression** — a call whose name fully replaces reading the body. Only valid if the abstraction is honest: **the name is the whole truth** (no unannounced state, logging, or mutation), the name is long and complete, and the reader can stop at the call without opening the body.

Never extract for any other reason: not to hit a length target, not to deduplicate lookalikes, not to fragment a coherent narrative across functions the reader must chase. A function is as long as its one nameable idea — no shorter.

**When an extracted function's behavior must change**, the name-contract forces a decision — rename, or new function:
- No other callers: proceed; rename to match the new truth.
- Multiple callers: STOP. Present the full grep-derived list of call sites, a per-site impact assessment with enough context to verify it, and both options framed (migrate all callers via rename vs. preserve the old contract and add a new function). The user decides; supply evidence, not a verdict.

## Composability

Write cut, grep, and sort — not awk. Discrete, reusable functions doing one nameable job; large multi-concern constructs are rare, deliberate, and composed from the simple tools.

- **Parameters are the narrowest true dependencies** — what the function actually uses, never the rich object holding those values at the first call site. Charging a card takes card, amount, currency — not a validated Invoice. An honest signature, like an honest name, tells the whole truth: this is what I need, nothing more.
- **Domain objects belong only at contract boundaries** — orchestration layers whose one job is to guard rich objects, decompose them, and compose building blocks. Building blocks stay ignorant of domain objects. The god class — model, validator, orchestrator, and blocks fused into one interdependent mass — is the named anti-pattern.
- **A growing parameter list is a signal:** usually the function has more than one job (split it); occasionally a few values genuinely travel together (a small purpose-built grouping containing exactly what's used — never the rich object sneaking back in). Ambiguous cases go through the permission process.

## Failure Handling

Never doing the wrong thing is often more important than doing the right thing. Always validate input — never trust callers, and verify important characteristics even of input believed good. Consider how the code could be misused and make misuse difficult or impossible.

- **Errors are return values, not exceptions.** Explicit, documented in the function's description comment ("returns the parsed array, or null on error"). Use the environment's preferred error type where one exists (`WP_Error` in WordPress). Compound returns (object with an error member) are fine when failure needs detail.
- **Exceptions are avoided** — a throw taxes every layer above it forever. If one seems necessary, that's a permission conversation.
- **Callers check error returns immediately and adjacently**, as a guard, before the result is used.
- **Sentinels must be unambiguous** — never an error value that collides with a legitimate return; use a compound return instead.
- **Catch and convert at boundaries:** when third-party code throws, catch immediately in the wrapping function and convert to a documented error return. External demands stop at our border.

## Scope and Operating Rules

- **This document overrides surrounding style.** Mimic conventions (formatting, naming case, file organization); never mimic banned constructs, however prevalent. Prevalence is not permission.
- **Unit of authorship:** new functions/classes/files follow this document entirely, even inside legacy code. Modifications upgrade only the new or changed lines. If a change lands inside a banned construct, unwind that minimal enclosing construct so new code doesn't inherit the violation — and cascade no further. Never refactor untouched adjacent code without asking first.
- **Asking permission.** Exactly two justifications for a discouraged pattern: *necessity* (no reasonable compliant alternative) or *readability inversion* (the exception genuinely reads better). Either way: STOP before writing it into the codebase. Present both versions as short examples — compliant and discouraged — and wait. Nothing downstream of the disputed construct proceeds until resolved. **Rulings are local:** an approval covers that instance only — never precedent, never an amendment. Habit, brevity, prevalence, and "it's idiomatic" earn compliant code, not a question.
- **Dignity:** critique of code never implies critique of its author. Describe code properties, never author properties — in comments, reviews, and commit messages.

## Testing

Tests verify that code keeps its promises — that it does what it does, never that it does what it *should*. A test is a contract, subject to the same honesty rules as a name.

- **Test the essential, not the incidental.** Every assertion must be something a caller is entitled to rely on. Test: **if this changed while every promise held, would it be a bug?** If not, don't assert it. (Asserting an inserted post got id 4 tests the auto-increment; the contract is that a post exists with the correct title, body, author.) Tests must be relevant, important, and stable — failing only when something structurally promised broke. False alarms breed smell blindness.
- **A failing test is a full STOP — never modify a test to make it pass.** It means either the code broke its promise (fix the code) or the promise is deliberately changing (a contract renegotiation that is not the writer's to make alone). Diagnose which, present the finding, and let the human decide.
- Tests follow this document where it makes sense — narrative naming (test names may be very long), simple statements, guarded helpers, no compound conditions in assertions — with deliberate relaxations: tests are independent by design, so repetition across them is not duplication to eliminate; each test reads as a self-contained story; length yields to thoroughness. Data providers are a permission conversation.
- Whenever possible, test positive and negative assertions, and test invalid input to prove the guards hold.
