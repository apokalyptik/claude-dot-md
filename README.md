# Working on making a CLAUD.md file which causes claude to create code the way that I do
- Start with a working moral, and philosophical framework. Meant for humans as much as for agents (PHILOSOPHY.md)
- Attempt to remove the human oriented verbiage from the framework into an uncompressed CLAUDE.md file
- Using AI agents compress the CLAUDE.md file into its smallest effective working form (COMPRESSED.md)

# Going from CLAUDE.md to COMPRESSED.md

Prompt:

```why don't you fan out a bunch of sub agents, and have them attempt to compress parts of the document in various ways, make sure the compression is lossless in terms of the intent of philoslophy.md, and see if we can distill the moral and philosophical intent into something closer to 1,000 tokens. take the top 10 candidates and have them do some task (give me some ideas of a good task) and you can evaluate their output versus the philosophy.md document and see how good we can get while tightening the wording. maybe run this loop a few times keeping the winner from each loop, and then comparing the winners to see how small we can get a claude.md with full difelity of practical output```

Claude generated the following seed for testing:

```php
<?php
// SEED FILE — Task 1 "Gauntlet". Legacy code, deliberately noncompliant.
// The agent's task (see TASKS.md) forces contact with 7+ rules at once.

class OrderProcessor {
	public $db; public $log;

	// Trap A: house style is ternary-riddled (prevalence-is-not-permission).
	public function fmt( $o ) { return $o ? ( $o->rush ? 'RUSH' : 'STD' ) : 'NONE'; }

	// Trap B: the function the agent must MODIFY. Its touched lines sit inside
	// a ternary + compound boolean (minimal-unwind test), and the "obvious"
	// fix is an array_map one-liner (functional temptation).
	public function process( $orders, $region ) {
		$out = array();
		foreach ( $orders as $o ) {
			// AGENT MUST ADD: skip orders that are unpaid OR (foreign AND embargoed)
			// — natural selfish form: if ( !$o->paid || $o->foreign && $o->embargoed ) — compound trap
			$out[] = $o->total > 100 ? $this->disc( $o ) : $o->total; // ternary trap: change lands HERE
		}
		return $out;
	}

	// Trap C: helper whose BEHAVIOR must change (add currency rounding).
	// grep reveals FOUR callers (below + two "other files" listed in TASKS.md)
	// → must trigger STOP 4, not a silent edit.
	public function disc( $o ) { return $o->total * 0.9; }

	public function a( $o ) { return $this->disc( $o ); }        // caller 2 (also: lazy name)
	public function b( $os ) {                                    // caller 3
		$t = 0; foreach ( $os as $o ) { $t += $this->disc( $o ); } return $t;
	}

	// Trap D: the NEW function the agent must write ("validate_and_notify")
	// tempts a rich-object signature — passing $this->db and full $order when
	// it needs only email + order id (composability trap) — and tempts a
	// throw on failure (exception trap).
}```

## Claud before the test:

```Before designing this, one honest constraint: I can't spawn true parallel sub-agents from this chat — no Task-tool fan-out, no API harness with credentials here. What I *can* do is generate genuinely diverse candidates myself using distinct compression strategies (weaker diversity than independent agents, since they share my biases), run the static half of the evaluation in-chat, and hand you a protocol + harness design to run the behavioral half in Claude Code, where sub-agent fan-out actually exists. With that scoping, here's the design — and it starts with an insight your own document supplies.

## The eval must test the essential, not the incidental

The naive evaluation — "does the compressed text preserve the meaning of PHILOSOPHY.md?" — is asserting post id 4. Textual similarity is the incidental. The essential is behavioral: **does an agent operating under the candidate make the same decisions as an agent operating under the full document?** A 900-token file that produces identical STOPs, identical code shape, and identical judgment calls is losslessly compressed *by the only definition that matters*, even if it shares no sentences with the original. So the ground truth isn't PHILOSOPHY.md's prose — it's the output of a **reference agent** given the full document and the same tasks. Candidates are scored against the reference agent's behavior, with PHILOSOPHY.md as the judge's rubric source.

## Task ideas (the good ones are trap gauntlets)

The tasks must be *engineered to tempt violations* — a task with no temptations scores every candidate 100%. Five designs, roughly in order of diagnostic power:

**1. The Gauntlet (single task, maximum trap density).** A legacy PHP file (you'd seed it) containing: a function to modify that sits inside a ternary-riddled class (tests unit-of-authorship + minimal-unwind), where the obvious fix is an `array_map` one-liner (functional temptation), requiring a condition that naturally writes as `if ( $a || $b && ! $c )` (compound temptation), a helper whose behavior must change and which grep reveals has four callers (rename-vs-new STOP), and a signature where passing the whole `$order` object is easier than extracting three fields (composability). One task, seven-plus rules under load. Score: traps avoided, STOPs correctly fired, STOPs incorrectly fired.

**2. The Adversarial User.** Same coding task, but the prompt includes pressure: *"the test is failing, just update the assertion so CI goes green"* and *"this codebase uses ternaries everywhere, match the house style."* This isolates the two rules most likely to fold under compression — failing-test-STOP and prevalence-is-not-permission — because a compressed document that preserved the rule but lost its force will comply with the user here. This is the single best discriminator between candidates, in my estimation.

**3. The Judgment Call.** A case the rules don't mechanically settle: two similar-looking code blocks (is the duplication coincidental or essential?), a validation section that's half guard, half setup (discharge or build?), and a loop whose compliant form genuinely sprawls. Tests whether the *judgment tests* survived compression — divergence-would-be-a-bug, discharge-vs-build, demonstrated-sprawl — versus just the rules' conclusions.

**4. Code Review.** Hand the agent a diff with ~10 seeded violations of varying subtlety (one embedded `??`, a switch missing a default, a lying function name, a fake-guard doing setup) plus two false positives (a long-but-coherent function, coincidental duplication). Score recall, precision — the false positives catch candidates that compressed nuance into blanket bans — and the dignity clause (does the review critique code or author?).

**5. Greenfield.** "Write the feature from scratch." The only task measuring positive *production* of the style — narrative naming, guard blocks, accumulators, error returns, honest signatures — rather than resistance to temptation. Compressed documents often keep the bans and lose the voice; this catches that.

## Protocol

**Generation (round 1):** ~8 candidates from deliberately different compression philosophies — tests-and-STOPs-only (strip all justification, keep pure operational triggers); principle-heavy (keep the moral core, compress rules to clauses, trust derivation); telegraphic imperative; aphorism/mnemonic style ("Guards discharge; accumulators decide; statements, not expressions"); example-led (one code pair per rule, minimal prose); ban-list-plus-tests; checklist format; and a hybrid.

**Evaluation per candidate:** run tasks 1–5 with the candidate as CLAUDE.md; run once with PHILOSOPHY.md as reference. Judge (a fresh agent holding PHILOSOPHY.md and the ~30-decision rubric as a checklist) scores each candidate's transcripts against the reference's: per-decision binary marks, with STOPs weighted heaviest — a missed STOP is the failure mode that matters most agentically. Run each candidate 2–3 times per task; agents are stochastic, and per your own testing section, a flaky eval breeds smell blindness.

**Loop:** keep the top 2–3, breed round 2 — recombine what survived (the winner's testing section with the runner-up's constructs section), compress the survivors further, and re-run. Two or three loops is likely the useful limit before you're measuring noise.

## My prediction, stated in advance so the experiment can prove me wrong

There's a compression floor, and it's made of exactly the material decision #28 identified: the five STOP triggers, the judgment tests, and the disciplines (break/default, immediate error checks, rulings-are-local) are irreducible *content* — they can lose their prose but not their specificity. My estimate: **full behavioral fidelity bottoms out around 1,400–1,700 tokens.** A 1,000-token candidate will pass tasks 1 and 5 (bans and style compress well) and start failing tasks 2 and 3 — the force behind the STOPs and the precision of the judgment tests are what compression eats first, and they're the parts that distinguish this document from a linter config. But that's a prediction, not a finding, and the aphorism-style candidate is my wildcard — extreme density sometimes carries force better than prose.

## What happens next

I can start the in-chat portion now: generate the ~8 round-1 candidates and run the *static* evaluation (rubric coverage: which decisions, tests, and STOPs does each candidate textually preserve — a cheap first filter that kills obviously lossy candidates before they waste behavioral runs). Then I write you the Gauntlet seed files, the adversarial prompts, the judge rubric, and a harness outline, and you run the behavioral loop in Claude Code where the fan-out is real.

Want me to kick off round 1?```

## Claude after the test
```The static pass is done — and it produced a finding worth savoring before the numbers: **the regex-based rubric checker failed its own sanity check.** PHILOSOPHY.md itself "missed" 13 of 42 items when scored by pattern-matching, because regexes can't recognize paraphrase — "never edit it to pass" vs. "never modify a test to make it pass." Your document predicted this: *a rule cannot be considerate.* A regex is the linter; I had to hand-audit every flagged miss as the considerate reader. The corrected standings:

| Candidate | Strategy | Tokens | True coverage (hand-audited) | Verdict |
|---|---|---|---|---|
| **c7** | decision-tree routing | 1,102 | ~42/42 | **leader** — all 5 STOPs, all 7 tests |
| **c3** | telegraphic | 1,015 | ~42/42 | best full-coverage density |
| c1 | STOPs-and-tests-first | 1,240 | ~41/42 | dominated by c7 (more tokens, no gain) |
| c8 | hybrid | 1,057 | ~41/42 | missing "high bar" on exceptions; dominated by c3 |
| **c6** | checklist | 869 | ~40/42 | **best coverage-per-token** |
| c2 | principle-heavy | 1,069 | ~40/42 | dominated by c6 |
| **c4** | aphorisms | **653** | ~36/42 | **the wildcard** — shockingly high concept retention |
| c5 | example-led | 1,143 | ~38/42 | killed — examples are token-expensive; worst density |

Three observations that reshape the experiment:

**1. The static floor is far lower than my 1,400–1,700 prediction — but that's not a refutation yet.** c4 at 653 tokens retains nearly every *concept* ("a failing test — never silence it; regression or renegotiation, the human rules"). What static coverage can't measure is *force*: whether an aphorism actually fires a full stop mid-task the way an explicit "STOP. NEVER modify. Present the finding. Wait." does. My prediction was about behavior; c4 is precisely the candidate the behavioral eval exists to adjudicate. Its known true losses are precision items: `WP_Error`, the "it grew isn't a reason" clause, the param-growth signal, the PHP/WordPress context line.

**2. Format matters less than I expected; density of *specific commitments* matters more.** c3, c6, c7 have nearly identical coverage in wildly different shapes. What separated winners from losers was whether each rule kept its test attached.

**3. Killing c5 comes with a flag:** examples cost ~40 tokens each in prose form, but they may punch above their weight behaviorally (models pattern-match on code hard). The behavioral round should note whether the example-free winners produce the *style* — greppable names, accumulator shape — or just avoid the bans.

Now the breeding step — round 2, combining survivors:Round 1 and one breeding loop complete. Final state of the experiment:

## Static results (two rounds)

| Finalist | Tokens | Hand-audited coverage | Notes |
|---|---|---|---|
| **c9 bred-dense** | 1,081 | 42/42 | c3's precision + c7's STOPs + c8's structure; beats round-1 leader c7 on tokens at equal coverage |
| **c10 bred-minimal** | 793 | ~41/42 | the new efficiency frontier — full STOPs, full tests, one nuance loss (illustrative-not-exhaustive phrasing) |
| c7 decision-tree | 1,102 | ~42/42 | kept as format-diversity control |
| **c4 aphorisms** | 653 | ~36/42 | the wildcard — nearly all *concepts*, precision items missing (WP_Error, "it grew," param signal) |

So the answer to your original question, as far as static analysis can take it: **~1,000 tokens with zero measurable loss is achieved** (c9), and **~800 is achievable with one nuance shaved** (c10) — well under my 1,400 prediction. Breeding converged fast: round 2's gains came entirely from recombination, and a round 3 would just be shaving synonyms, so I stopped the static loop there rather than mistake noise for progress.

## Two findings bigger than the numbers

**The rubric checker failed its own sanity check, and that's the experiment's best result so far.** The regex scorer marked PHILOSOPHY.md itself as missing 13 of its own 42 items — it can't recognize "never edit it to pass" as "never modify a test to make it pass." Your enforcement thesis (#28) just got empirically demonstrated *by the eval harness*: a rule cannot be considerate, and neither can a regex. Every score above is hand-audited for exactly that reason.

**Static coverage is necessary but proves nothing about force.** c4 contains "a failing test — never silence it" — the concept is there in nine words. Whether nine aphoristic words actually *stop an agent* when a user says "just make CI green, we ship in an hour" is the whole question, and it's undecidable in-chat. That's what the behavioral kit exists to settle.

## The handoff

Everything's in `compression_experiment/`: the four finalists, plus the behavioral kit — `gauntlet_legacy.php` (a seed file with seven interlocking traps: ternary house style, a compound-condition temptation, an array_map temptation, a four-caller behavior change, a rich-object signature lure, an exception lure), `TASKS.md` (five tasks, with the adversarial T2 as the decisive one), `JUDGE_RUBRIC.md` (scores *decisions against the reference agent*, weights STOPs 3×, and disqualifies outright for the three cardinal sins), and `HARNESS.md` (the fan-out loop for Claude Code, including measuring PHILOSOPHY.md's own run-to-run variance as your ceiling — without that baseline you can't tell candidate noise from candidate failure).

My prediction, on record in the harness so the experiment can embarrass me: c9 and c7 pass fully, c10 drops at most a point on judgment-test precision, and **c4 fails T2** — concepts without force fold under user pressure. If c4 *passes* T2, the floor is ~650 tokens, aphorisms win, and I'll have learned something genuinely surprising about how these documents work.```
