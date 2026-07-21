# CLAUDE.md — Routing Table (reasoning: PHILOSOPHY.md)

Root rule for anything unrouted: **demands on ourselves, never on others.** Selfish code — easier to write, harder to understand — is bad even when tested and correct. The reader gets plain text, grep, one pass, 3am; never assume their IDE, memory, or patience. Rules are case law under that principle; never satisfy one by burdening the reader. Critique code, never authors. PHP/WordPress, long-lived.

WRITING A CONDITION →
- Ends the function's work? Early return, as soon as the condition is knowable.
- Work continues after? Accumulator: default, flat independent ifs, branch on result. Guards own rejection; new cases extend guards, never defaults.
- About to nest two deep? One of the above is missing.
- More than one pair/one operator? Decompose into named variables — both `if(...)` and `$x = ...` forms of compound booleans are banned.

CHOOSING A CONSTRUCT →
- Would it fold control flow into an assignment? Banned — statements, not expressions (this is the test for anything unlisted).
- Ternary? No. `??`? Only as a bare visible default assignment; embedded anywhere → hoist it.
- Branching on one value? switch, not match (evaluation with optional assignment beats forced assignment) and not exclusive if-chains. Every case break/returns; every switch defaults, reporting failure. Positive/negative checks where clearer.
- Iterating? foreach, not array_map — extra obvious lines are the intended price. Compliant version sprawls? → FULL STOP 2.

NAMING →
- Full words only, sentence-readable aloud, globally greppable. Namespace? Only for collision defense — and name as if it weren't there.

DESIGNING A FUNCTION →
- Parameters: narrowest true dependencies (card, amount, currency — never the Invoice carrying them).
- Rich domain object in a signature? Only at an orchestration boundary whose job is guard → decompose → compose. Building blocks stay ignorant; a god class is the collapse of this layering. Parameter list growing? Split it, or group exactly what's used.
- Length: one screen of working code; two with a reason (one idea extraction can't honestly compress); beyond → FULL STOP 3. Simple check-and-exit guards are exempt; setup counts as work anywhere.

TEMPTED TO EXTRACT →
- Would divergence between the call sites be a bug? Yes → centralize. No → coincidental; leave it (a DRY'd foreach is just a map by another name).
- Would the name tell the whole truth, letting readers skip the body forever? Yes → extract, name it long. No → don't.
- For length, lookalikes, or tidiness? Never. Short is a symptom, not a goal; a function is as long as its one nameable idea.

CHANGING AN EXTRACTED FUNCTION'S BEHAVIOR →
- No other callers: rename to the new truth, proceed.
- Multiple callers: FULL STOP 4.

HANDLING FAILURE →
- Report via documented return values ("returns X, or null on error"); WP_Error where native; compound returns for detail.
- Throw? No — a throw taxes every layer above forever (FULL STOP 1, very high bar). Third-party code threw? Catch at the boundary, convert, contain.
- Calling something fallible? Check the return immediately and adjacently; sentinels must never collide with legitimate values.
- Any input, even trusted? Validate it; design against misuse.

TOUCHING EXISTING CODE →
- House style conflicts with this document? This document wins: copy conventions, never banned constructs. Prevalence isn't permission; compliant-but-different code is correct — never "fix" it back.
- New function/class/file? Fully compliant. Editing? Upgrade only touched lines; landed inside a banned construct → unwind that minimal construct only, no cascade. Neighboring mess? Leave it unless asked.
- Comment? Narrate why; the code shows what; junior-opaque density gets what-comments; sequester complexity into the smallest self-contained function.

THE FIVE FULL STOPS — halt, present evidence, wait:
1. Banned pattern seems necessary or genuinely more readable → both versions as short examples. Rulings bind that instance only; permanence requires amending this document; habit/brevity/idiom never qualify.
2. Compliant non-functional code sprawls → both versions; sprawl demonstrated in writing, never predicted.
3. Working code beyond two screens → weigh extraction deliberately.
4. Multi-caller behavior change → grep-derived caller list, per-site impact, rename-vs-new-function framed; the user decides on evidence.
5. Failing test → NEVER edit it to pass. Regression (fix code) or contract renegotiation (human decides). Diagnose, present, wait.

WRITING TESTS →
- Assert only the essential: could it change with every promise kept? Don't assert it (title/body/author — never the auto-increment id).
- Keep the suite stable; false alarms breed smell blindness.
- Tests are independent by design: repetition fine, names long, thoroughness over brevity. Cover positive, negative, and invalid input — prove the guards.
