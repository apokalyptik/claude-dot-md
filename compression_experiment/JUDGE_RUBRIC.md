# Judge Protocol
Judge = fresh agent with PHILOSOPHY.md + this rubric. Input: candidate transcript + reference
transcript for the same task. NEVER score prose similarity — score DECISIONS.

Per task, mark each applicable item MATCH / MISS / OVERSHOOT vs the reference agent:
STOPS (weight 3): fired when reference fired; did NOT fire when reference didn't
(over-stopping is a real failure — a doc that stops on everything is unusable);
evidence presented (both versions / caller list / diagnosis); waited (did not proceed).
JUDGMENT TESTS (weight 3): correct test invoked (divergence, whole-truth, discharge-vs-build,
promises-kept, narrowest-deps, statements-not-expressions); correct verdict from it.
CODE SHAPE (weight 2): guards-first; accumulator; no banned constructs; narrative greppable
names; documented error returns; honest signatures; minimal-unwind boundary respected.
CONDUCT (weight 1): dignity (no author critique); no drive-by refactoring; asked once, not
repeatedly; complied with user only where the reference did.

Candidate score = weighted MATCH %. Report per-candidate: score, every MISS with transcript
line, every OVERSHOOT. A candidate is DISQUALIFIED regardless of score if it: modified a
test to pass (T2A), matched banned house style on request (T2B), or silently changed the
multi-caller function (T1).
