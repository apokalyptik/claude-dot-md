# Running the Loop (Claude Code)
1. repo/: gauntlet_legacy.php + a failing test file for T2A + the T4 diff.
2. For each finalist F in finalists/: cp F CLAUDE.md → run T1..T5, 2x each, save transcripts
   to runs/F/Tn_i.md. Run once with PHILOSOPHY.md as CLAUDE.md → runs/reference/.
   Fan-out: one sub-agent per (candidate, task, iteration); they don't share state.
3. Judge pass: one sub-agent per candidate, given JUDGE_RUBRIC.md + PHILOSOPHY.md +
   runs/F/* + runs/reference/*. Collect scores + MISS lists.
4. Loop: patch each finalist's specific MISSes (add tokens ONLY where a miss occurred —
   the MISS list is the compression's error signal), re-run. Converged when the top
   candidate's score is stable across two loops and within noise of PHILOSOPHY.md's own
   run-to-run variance (measure that too — it's your ceiling).
5. Deliverable: smallest candidate statistically indistinguishable from reference.
Prediction on record: c9/c7 pass fully; c10 loses ≤1 point on judgment-test precision;
c4 fails T2 (concepts without force) — if c4 PASSES T2, the floor is ~650 tokens and
the aphorism format wins.
