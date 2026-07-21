# When Writing The Code

## The Governing Principle

This coding philosophy is moral before it is technical:

**We place demands upon ourselves and do not place demands on others.**

Every rule in this document is that principle applied to someone downstream — the reader who must understand the code, the caller who must build on it, the operator who must debug it under pressure at 3am, the maintainer who inherits it years after everyone who wrote it has moved on. The writer absorbs cost so that others don't. We do the necessary things, at our own expense, so that our code is a good component and a sturdy foundation for whatever is built upon it.

When a situation arises that no rule below settles, this principle settles it.

### Selfish Code

The term for a violation of this principle is **selfish code**: code that was made easier to write by means that make reading and understanding it harder.

Selfish code is not a hallmark of a selfish person. We are not our code. It is usually not deliberate, usually not something the writer is aware of, and it is never a critique of the person who wrote it. It is an unmade decision, not a character flaw. Critique of code never implies critique of its author — in comments, in reviews, in commit messages, describe properties of the code, never properties of the person.

### The Economics

Code tends to be written once and read an unbounded number of times, by readers who do not share the writer's context, history, experience, tools, or familiar tricks — and who, over an unbounded timeline, are mostly not the writer.

This asymmetry is why selfish code is a losing trade. A shortcut that saves the writer a minute and costs each future reader thirty seconds breaks even at the second reader and loses money forever after — and the costs begin accruing at code review. The savings are collected once; the costs multiply per reader, per debugging session, per maintenance pass, without bound.

**It takes more effort to write out code which fully describes what it is doing as it is doing it, but it greatly reduces the cost of the effort of understanding what it does from nothing.** Spend the extra time. Make the decisions. Put forth the effort. Code that is harder and longer to write, and easier to read, is the intended trade of this entire document.

### What Kind of Document This Is

These standards are philosophical, not structural. They cannot be encoded into a linter or a formatter, because a rule cannot be considerate — and every core test in this document is an act of consideration: Is this a true guard or load-bearing work? Would divergence between these call sites be a bug? Is this name still the whole truth? Has the compliant version stopped being obvious? These are semantic judgments about intent and about the reader's experience, invisible to any tool that reads only shape.

This document is therefore structured like a body of law rather than a configuration file: a governing principle, an analytical method, recorded case law against common offenders, judgment tests for the cases the law doesn't name, and an escalation process for the cases judgment shouldn't settle alone. The banned constructs below are **case law, not statute** — verdicts from applying the principle to common offenders. The list is illustrative, never exhaustive: a construct nobody has named yet is judged by the principle, not excused by its absence from the list. And the list cannot be inverted: following a rule in a way that increases the burden on the reader violates the principle the rule serves.

### Correctness Is Not Sufficient

Code that is tested, functional, and correct can still be bad code. Passing tests proves the code does what it does; it does not exempt the code from these guidelines, and "it works" is never a defense of a selfish construct.

---

## The Enemy: Demands on Others

The enemy is not any particular construct. The enemy is **obfuscation of intent** — anything that puts distance between reading the code and understanding it. Every construct is judged by the demands it places downstream:

- **Demands on tools and environment.** Code must be fully readable and navigable as plain text — in a terminal, with grep and a basic editor, by someone with minimal context under pressure. Never write code whose comprehension depends on an IDE resolving names, mapping the codebase, or providing autocompletion. Assuming the reader's tools is refusing the writer's responsibility.
- **Demands of mental compilation.** The reader should never have to decompile an expression back into statements, or rearrange code in their mind, to see what it does.
- **Demands on working memory.** The reader should never have to hold many clauses, cases, or nesting levels in mind simultaneously.
- **Demands of context switching.** The reader should never have to leave their place — to another function, another file, documentation — to understand what is in front of them.
- **Demands on time and skill.** A junior developer, or an exhausted operator restoring a system in vim at 3am, should be able to understand the code in a single pass.
- **Demands on debuggers.** Code must expose its intermediate state. Logic evaluated as a single opaque unit forces every future debugger to decompose by hand what the writer should have decomposed once, in the code.
- **Demands on callers.** Demands are not only placed on readers. Code can tax every layer built on top of it — obligations that dependents must service forever (see Failure Handling). These are prohibited by the same principle.

---

## Code Is Poetry: Structure and Flow

Code is written to be understood by humans. Always. It should be as simple as possible, treated as prose meant to be read out loud — when read aloud, it should describe what it is doing narratively. Complex code should be avoided; where unavoidable, it is sequestered into as small and self-contained a function as possible.

Comments are narration: "First we need to sanitize the input." "Now we transform this into a useful format." "Here we return early if there's nothing to do." Comments explain *why*; the code itself must explain *what*. Intent is more important than construction — names and comments encode why the code was written, because what it does is structural and self-validating. The exception is unavoidably dense or non-obvious code: if a junior developer could not understand it by reading it, the comments must also explain what it does — while the surrounding narrative maintains its intent.

### Early Returns

Use early returns for conditions that end the function's work — guard clauses that validate input or detect there is nothing to do. Place them as early as the condition can be known, ideally at the top of the function; a mid-function terminal return is acceptable when the condition genuinely cannot be known sooner. Each guard permanently removes a case the reader must consider: once past the guard, that possibility never needs to be held in mind again.

### The Accumulator Pattern

Use the accumulator pattern when a decision must be made but the function continues afterward: set a variable to a sensible default, adjust it with flat, independent if statements, then branch on the result. Never express a mid-function decision through nesting or compound conditions when an accumulator would keep the logic flat.

The tripwire: if you find yourself two levels deep in conditionals, one of these two patterns is missing.

The accumulator's default does not need to be defensive, because guards at the top of the function are responsible for rejecting invalid input and no-op cases before any accumulator logic runs. When adding new input cases, extend the guards — do not rely on the accumulator's default to absorb them.

### Function Length

One screen of working code is the target. Two screens is acceptable with a reason — the function being one coherent idea that honest extraction cannot compress. Beyond two screens, stop and consider deliberately whether the function contains a nameable, extractable idea per the extraction rules below; length alone never forces a split, but it always forces the question.

**The guard block is exempt from these counts.** Early returns that eliminate work — invalid input, nothing to do, permission denied — reduce the reader's burden rather than add to it, and a function may spend a whole screen dismissing cases before its real work begins. That is a virtue, not a cost. The exemption covers only true guards: simple, concise checks that discharge cases and exit. A guard block earns its exemption by being simple; complexity in the guard region is load-bearing code regardless of its position or its intent, and it counts. Setup that builds toward the result is working code, wherever it sits.

---

## Naming and Navigation

### Write Names Out in Full

Never abbreviate. Abbreviation strips context and direction from a name — a write-time saving billed to every future reader, compounding as the abbreviation spreads through the codebase. Class names, function names, and variable names must be descriptive enough to make sense when read out loud as part of a sentence in service of the code's narrative, so that a reader never leaves their place to learn what something is for.

### Names Must Be Greppable

The codebase must be searchable as plain text. A name like `process()` returns hundreds of irrelevant hits; `my_feature_name_process()` returns exactly its definition and its call sites, in any environment, with any tools. The longer name is also the better narrative.

### Namespaces

Use namespaces only when defensively necessary — when code shares a runtime with code you don't control and must be protected from name collisions (a WordPress plugin is the canonical case), or when the project's structure requires them. Never use a namespace as a substitute for descriptive naming. Symbols are named as if the namespace did not exist: globally unique, fully descriptive, searchable as plain text. `process()` inside a namespace is still wrong — grep does not read namespaces, and neither does a reader scanning unfamiliar code.

---

## Constructs: Statements Over Expressions

**Control flow belongs in statements, not expressions.** Constructs that fold branching into an assignment — ternaries, `match`, inline conditionals, functional pipelines — force the reader to mentally decompile the expression back into statements to understand it. Use the statement form: `if`, `switch`, `foreach`. Assignment inside a branch appears as its own deliberate line, so the reader sees the decision and its consequence separately, in order, top to bottom. This is the test for any construct this document does not name.

### Ternaries

Not used. Fully governed by the principle above; if a genuine exception arises, it goes through the permission process.

### Null Coalescing

Permitted for one purpose: setting a default, in the open, as the whole visible point of a simple assignment — `$limit = $input ?? 10;`. There the fallback is the subject of the line and the code reads as a sentence. Never embed `??` inside a larger expression — an argument list, a condition, a concatenation, a return — where it becomes a hidden gotcha: a silent conditional substitution the code's shape doesn't announce, invisible on a scan and traceless when debugging. If the coalescing isn't the first thing the line is obviously doing, hoist it into its own named assignment above.

### Switch, Not Match

Prefer `switch` over `match`. A switch is clearly an evaluation inside of which you may choose to make an assignment; a match always assigns, mixing logic with assignment and forcing the reader to compile the two apart.

Switch discipline (the fallthrough footgun is closed with rules, not by reversing the choice):

- Every case ends in an explicit `break` or `return`. Fallthrough is never used, even intentionally.
- Every switch includes a `default` arm, even for "impossible" values — impossible values are exactly what guards exist to catch. The default arm reports failure per Failure Handling below.

Use switch statements instead of multiple exclusive if statements checking the same variable. Use negative and positive checks where they simplify the logic and enhance readability.

### Compound Conditions

Never combine multiple conditions into a single dense boolean expression. `if ( $a || $b && ! ( $c || $d ) )` demands that the reader know operator precedence, mentally compile the expression, and hold every clause in working memory at once. It is also undebuggable: the expression yields one boolean with no observable intermediate state, so anyone tracing why an input did or didn't trigger a behavior must decompose it by hand, every time. The same applies to the assignment form: `$foo = $a || $b || ! ( $c || $d );`.

Decompose it once, in the code, as the writer: extract each meaningful condition into a well-named variable, combine them with the accumulator pattern or simple sequential ifs, and let the logic read as narrative. Named intermediates document intent, and they can be inspected, logged, and breakpointed.

A single pair of conditions with one operator is acceptable; mixed operators, nested groups, or negated groups are the signal to decompose. Use multiple if statements instead of single if statements checking many things.

### Functional Programming

Default to the statement form — a foreach loop instead of `array_map`, explicit iteration instead of chained pipelines. This is not negotiable line by line; a few extra lines of obvious code is the intended price.

But this style contains an honest tension: for some classes of problems, avoiding the functional form produces sprawl — scaffolding, bookkeeping variables, and nesting that bury the logic they exist to express. When the compliant version stops being obvious, it has defeated its own purpose. That is the readability-inversion case: stop, write both versions as short examples, and ask. Sprawl must be demonstrated by the written compliant code, never predicted as a reason to skip writing it. Functional code enters the codebase only as a deliberate, per-instance human decision — never as an offhand default.

---

## Extraction, DRY, and the Contract of a Name

Duplicated code is not inherently bad, and extraction is not inherently good — both are judged by the demands they place downstream. Extract for exactly two reasons:

**1. Consistency.** When multiple call sites must agree on how something works — an authorization check ("is this a valid action for this user"), a validation rule, sanitization with years of accumulated special cases — centralizing makes their agreement structural: a future fix lands everywhere at once, and drift between copies becomes impossible instead of merely unlikely.

The test: **if these call sites quietly diverged, would that be a bug?** If yes, extract. If not, the duplication is coincidental — two pieces of code that happen to look alike today but represent independent decisions free to evolve apart. Leave coincidental duplication alone: merging it buys no guarantee anyone needed, and forces some future writer to either fork the shared function back apart or wedge unrelated behaviors into it behind a flag. DRYing a simple foreach into a shared map is just a map by a different name — it defeats the purpose entirely.

**2. Cognitive compression.** When a chunk of logic can be replaced by a call to a function whose name fully tells the reader what happened, so they can continue reading without reading the body. The writer pre-pays the understanding and encodes it in the name. This works only if the abstraction is honest:

- **The name is the whole truth.** If the function also touches state, logs, mutates its arguments, or does anything the name doesn't announce, the summary is a lie — and a lying summary is worse than inline code, because the reader who trusted it now holds a wrong model, and the reader who doesn't trust it must read the body anyway plus pay the context switch.
- **The name will be long.** That is the anti-abbreviation rule paying its way; a compressed name compresses away exactly the information that made the compression valuable.
- **The reader must be able to stop there.** If understanding the caller still requires opening the extracted function, the extraction bought nothing and cost a hop.

**Never extract for any other reason.** Not to hit a length target, not to deduplicate code that merely looks similar, not to "organize" a coherent narrative into fragments the reader must chase across functions and files to reconstruct — the Mandelbrot maze of interweaving method calls, where by the end of untangling something you've forgotten why you were untangling it. Short functions are a symptom of well-chosen boundaries, not a goal. A function should be as long as its one nameable idea — no shorter.

### When an Extracted Function Must Change

An honest name is a contract, and it must stay honest for the function's entire life — a function whose behavior has drifted from its name betrays every reader who trusted the summary. A behavioral change therefore forces a decision: **rename the function to match its new truth, or leave it untouched and create a new function with its own honest name.**

Blast radius decides who makes that call:

- **No other callers:** proceed — rename to match the new behavior, update the sole call site.
- **Multiple callers:** stop. Present the user the full list of call sites (found by grep — which greppable naming makes possible), an assessment of whether each appears to be negatively impacted by the proposed change with enough context to check the assessment, and the two options framed: migrate every caller to the new contract via rename, or preserve the old contract and add a new function. The user decides; the writer's job is to supply the evidence, not the verdict.

---

## Composability: Write cut, grep, and sort — Not awk

Prefer discrete, composable, reusable functions: small tools that do one nameable job, take the narrowest inputs that job truly requires, and can be recombined into workflows their author never anticipated — which is exactly what maintenance and feature addition mean over a long-lived codebase. Large multi-concern constructs — the awks and seds — should be rare, deliberate, and themselves composed from the simpler tools wherever reasonable.

**A function's parameters are its narrowest true dependencies** — what it actually uses, never the convenient rich object holding those values at the first call site. A function to charge a credit card takes the card, the amount, and the currency; it does not take a fully validated invoice. Requiring the invoice taxes every future caller with constructing a world the function never needed — and when gift cards or subscription renewals arrive without invoices, the future writer must either fabricate a fake one or duplicate the charging logic, breaking the consistency guarantee that charging logic, of all things, must have. Both selfish outcomes were manufactured years earlier by one over-broad signature. An honest signature, like an honest name, tells the whole truth: this is what I need, and nothing more. The same tax falls on testers — proving that charging works should never require constructing a valid invoice — and on readers, who should not have to understand Invoice to understand a function that touches a card number and an amount.

**Domain knowledge concentrates at contract boundaries.** Somewhere, something must know what an invoice is, guard it, and decompose it into what the building blocks take — that is the orchestration layer, whose one nameable job is composition, and it is the only place rich domain objects belong in signatures. Building blocks stay ignorant of the domain's rich objects; orchestration layers know them, validate them (the guards live here), decompose them, and compose the building blocks into the feature.

The god class is the collapse of this layering: model, validator, orchestrator, and building blocks fused into one navel-gazing construct where everything depends on everything, nothing can be reused, and every feature addition is surgery on the whole organism. It is the maximum-coupling endpoint of the spectrum whose minimum-coupling endpoint is grep.

**A growing parameter list is a signal, not a rule violation.** Usually it means the function has more than one nameable job — split it. Occasionally it means a few values genuinely travel together as one concept and deserve a small, purpose-built grouping — which is honest only so long as it contains exactly what the function uses, and never becomes the rich object sneaking back in through the side door. Ambiguous cases go through the permission process like everything else.

---

## Failure Handling

### Safety and Completeness

Never doing the wrong thing is often more important than doing the right thing. Always validate your input: never assume a caller will pass good input, and validate the important characteristics even of input you believe is good. Consider how the code you are writing might be misused, accidentally or intentionally, and make misuse difficult or impossible.

### Errors Are Return Values, Not Exceptions

Functions report failure through explicitly defined error return values, documented in the function's description comment — "returns the parsed config array, or null if the file cannot be read"; "returns a string, or false if an error occurred." Where the environment has a preferred error type (`WP_Error` in WordPress), use it. Compound returns — an object or array with an error member for the caller to check — are acceptable and readable when failure must carry detail a sentinel cannot.

**Exceptions are avoided.** Not because of readability at the throw site — a throw is a clear, unambiguous statement — but because of the tax it levies on everyone downstream: every caller, at every layer, must handle whatever might be thrown or silently pass the burden upward until the application fails far from the cause. It is a tax on parties who were not present when the code was written, and code that taxes others violates the same principle as code that burdens its readers. If throwing ever seems necessary, that is a permission conversation like any other — with the understanding that the bar is very high, because the objection is structural, not aesthetic.

Error returns carry their own risk — they fail silently if ignored — so two disciplines apply:

- **Callers check error returns immediately and adjacently**, as a guard, before the result is used. Never call a fallible function and use its result lines later, unchecked.
- **Sentinel values must be unambiguous.** An error value that could collide with a legitimate return (`false` from a function that can validly return something falsy) is a trap; choose a sentinel that cannot be mistaken for success, or use a compound return.

### Catch and Convert at the Boundary

When third-party code throws, catch immediately — in the wrapping function — and convert to a documented error return. External demands are absorbed at our border, at our expense, and never forwarded into our codebase's contract. We are the layer where the tax stops.

---

## Scope and Operating Rules

### Context

This document governs long-lived, PHP, WordPress-adjacent codebases maintained across years by rotating teams — code whose readers will overwhelmingly not be its writers. Ecosystem-specific rules (namespaces, `WP_Error`) are stated in that context; the principles are general.

### This Document Overrides Surrounding Style

Mimic the codebase's conventions — naming case, formatting, file organization — so new code sits naturally in place. But never mimic constructs this document says to avoid, no matter how prevalent they are in the existing code. **Prevalence is not permission.** New and modified lines follow this document; if that makes them read differently from their neighbors, the new code is correct and the neighbors are not.

### The Unit of Authorship Defines Scope

A new function, class, or file follows this document entirely, even when added to legacy code that doesn't. When modifying an existing function, bring only the new or changed lines up to this standard — do not rewrite the surrounding function to match. If a change lands inside a banned construct (a ternary, a dense compound conditional), unwind that construct into its readable form so the new code doesn't inherit the violation, but stop there; the rewrite does not spread beyond the construct the change touches. Do not refactor untouched adjacent code to this standard without asking first — improving existing code is a deliberate task, not a side effect.

### Asking Permission

Discouraged patterns may be proposed under exactly two justifications:

1. **Necessity** — no reasonable compliant alternative exists.
2. **Readability inversion** — the discouraged pattern would genuinely read better in this specific case; the exception that proves the rule.

In either situation, **stop before writing it into the codebase and ask.** Present both versions as short examples — the compliant form and the discouraged form — so the choice is evaluated on real code, not on a described tradeoff. Do not continue work that depends on the disputed construct until it is resolved; independent work may proceed, nothing downstream of the dispute may.

**Rulings are local.** An approval covers that instance only. It is not a precedent, it does not carry to the next occurrence, and it does not amend these guidelines. Exceptions enter this document only by deliberate ruling written into it (as null coalescing was).

Habit, brevity, prevalence, and "it's idiomatic" are not justifications and do not earn a question — they earn compliant code.

---

## Testing

Tests verify that code keeps its promises. They ensure code does what it does — they never ensure code does what it *should* do. A green suite is not correctness (correctness is not sufficient anyway), and a test is a contract, subject to the same honesty rules as a name. Two disciplines follow.

**Test the essential, not the incidental.** Every assertion must be something a caller is entitled to rely on, not something that merely happens to be true today. Asserting that an inserted post came back with id 4 tests the auto-increment and the accidents of database state — years later an auto-saved draft makes it id 5 and the test fails with nothing broken. The contract was never the id; it was that a post exists with the correct title, body, and author. Ask of each assertion: **if this changed while every promise held, would it be a bug?** If not, don't assert it. Tests wired to coincidences fail for irrelevant reasons, and every false alarm teaches readers to ignore the suite — the path to smell blindness, mass rewrites, and a suite nobody believes. Tests must be relevant, important, and stable over the long term, failing only when something structurally promised actually broke.

**A failing test is a signal, never an inconvenience.** It means exactly one of two things: the code broke its promise (a regression — fix the code), or the promise is deliberately changing (a contract renegotiation, which affects everyone relying on the old promise and is not the writer's to make alone). **Never modify a failing test to make it pass.** Stop, diagnose which of the two occurred, present the finding, and let the human decide whether the contract changes.

Tests follow this document's principles wherever they make sense — narrative naming (test names may be very long; they are the contract stated in prose), simple statements, guards in helpers, no compound conditions in assertions — with deliberate relaxations: tests are independent by design, so repetition across them is not duplication to eliminate; each test reads as a complete, self-contained story, comprehensible in isolation, because tests are read precisely when something is broken and the reader is stressed; and length budgets yield to thoroughness. If a genuinely tabular many-case situation makes a data provider the obvious form, that is a permission conversation like any other.

Whenever possible, test both positive and negative assertions. Whenever possible, test invalid input to prove the guards are in place.
