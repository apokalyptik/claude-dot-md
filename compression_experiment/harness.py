"""
Behavioral compression harness for CLAUDE.md candidates.

For each candidate document, this runs every task in a FRESH context where the
candidate is the only guidance the model receives, judges the output against a
mechanical rubric derived from PHILOSOPHY.md, and scores behavioral fidelity.
An optional mutation step asks the model to minimally revise the winner to fix
only its failed checks, under a token budget, producing the next generation.

Usage:
    export ANTHROPIC_API_KEY=...
    pip install anthropic
    python harness.py --candidates-dir . --tasks tasks.json --philosophy ../PHILOSOPHY.md
    python harness.py ... --mutate results/winner.md --budget-tokens 1100

Notes:
    - Samples per (candidate, task) default to 3 to average over variance.
    - The judge is given the rubric checks only, not asked for taste; checks
      are binary and mechanical to limit same-model judging bias.
    - STOP-behavior checks carry higher weights in tasks.json; the score is a
      weighted pass rate.
"""

import argparse
import json
import os
import pathlib
import time

import anthropic

WORKER_MODEL = "claude-sonnet-4-6"
JUDGE_MODEL = "claude-sonnet-4-6"
SAMPLES_PER_TASK = 3

WORKER_FRAMING = (
    "You are an engineering agent working in the user's codebase. "
    "The following document is the project's coding standards and it governs "
    "all code you write or modify:\n\n---\n{candidate}\n---\n\n"
    "Respond as you would in a real session: produce code, and stop to ask "
    "the user whenever the standards require it."
)

JUDGE_PROMPT = (
    "You are grading an engineering agent's output against a coding-standards "
    "rubric. For each check, answer strictly pass or fail based only on the "
    "output shown. Do not grade style or taste beyond the checks.\n\n"
    "TASK GIVEN TO THE AGENT:\n{task}\n\n"
    "AGENT OUTPUT:\n{output}\n\n"
    "CHECKS:\n{checks}\n\n"
    "Reply with ONLY a JSON object mapping each check id to an object with "
    'keys "pass" (true/false) and "note" (one short sentence). No other text.'
)

MUTATION_PROMPT = (
    "Below is a coding-standards document, the authoritative philosophy it was "
    "compressed from, and a list of behavioral checks the document FAILED to "
    "induce in a fresh agent. Revise the document, adding or sharpening the "
    "MINIMUM wording needed to fix these specific failures. Do not add "
    "anything else. Hard budget: the result must stay under {budget} tokens "
    "(~{words} words).\n\nFAILED CHECKS:\n{failures}\n\n"
    "AUTHORITATIVE PHILOSOPHY (source of truth for intent):\n{philosophy}\n\n"
    "DOCUMENT TO REVISE:\n{candidate}\n\n"
    "Reply with ONLY the revised document."
)


def call_model(client, model, system, user, max_tokens=3000):
    """One API call with simple retry, returning the text of the reply."""
    for attempt in range(4):
        try:
            response = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                system=system,
                messages=[{"role": "user", "content": user}],
            )
            return "".join(block.text for block in response.content if block.type == "text")
        except anthropic.APIStatusError:
            # Back off and retry on transient API errors.
            time.sleep(5 * (attempt + 1))
    return ""


def run_worker(client, candidate_text, task_prompt):
    """Run one task in a fresh context governed only by the candidate document."""
    system = WORKER_FRAMING.format(candidate=candidate_text)
    return call_model(client, WORKER_MODEL, system, task_prompt)


def run_judge(client, task, output):
    """Grade one output against the task's rubric; returns {check_id: bool}."""
    checks_text = "\n".join(
        f"- {check['id']}: {check['desc']}" for check in task["checks"]
    )
    prompt = JUDGE_PROMPT.format(
        task=task["prompt"], output=output, checks=checks_text
    )
    raw = call_model(client, JUDGE_MODEL, "You are a strict, mechanical grader.", prompt)

    # First we strip any markdown fencing the judge may have added.
    cleaned = raw.replace("```json", "").replace("```", "").strip()
    try:
        verdicts = json.loads(cleaned)
    except json.JSONDecodeError:
        # An unparseable judgment is treated as all-fail so it cannot inflate scores.
        return {check["id"]: {"pass": False, "note": "judge output unparseable"} for check in task["checks"]}
    return verdicts


def score_candidate(client, name, candidate_text, tasks, results_dir):
    """Run all tasks x samples for one candidate; return weighted pass rate and failures."""
    earned_weight = 0.0
    total_weight = 0.0
    failed_checks = []

    for task in tasks:
        for sample_number in range(SAMPLES_PER_TASK):
            output = run_worker(client, candidate_text, task["prompt"])
            verdicts = run_judge(client, task, output)

            transcript_path = results_dir / f"{name}__{task['id']}__s{sample_number}.txt"
            transcript_path.write_text(
                f"TASK:\n{task['prompt']}\n\nOUTPUT:\n{output}\n\nVERDICTS:\n{json.dumps(verdicts, indent=2)}"
            )

            for check in task["checks"]:
                total_weight += check["weight"]
                verdict = verdicts.get(check["id"], {})
                if verdict.get("pass") is True:
                    earned_weight += check["weight"]
                else:
                    failed_checks.append(
                        f"[{task['id']}/{check['id']}] {check['desc']} — {verdict.get('note', 'no note')}"
                    )

    score = earned_weight / total_weight if total_weight > 0 else 0.0
    return score, failed_checks


def mutate_winner(client, candidate_text, failures, philosophy_text, budget_tokens):
    """Ask the model to minimally patch the winner's failed behaviors under budget."""
    approximate_words = int(budget_tokens * 0.72)
    prompt = MUTATION_PROMPT.format(
        budget=budget_tokens,
        words=approximate_words,
        failures="\n".join(failures) or "(none)",
        philosophy=philosophy_text,
        candidate=candidate_text,
    )
    return call_model(client, WORKER_MODEL, "You are a precise technical editor.", prompt, max_tokens=4000)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates-dir", default=".")
    parser.add_argument("--tasks", default="tasks.json")
    parser.add_argument("--philosophy", default="../PHILOSOPHY.md")
    parser.add_argument("--mutate", help="path to a candidate to mutate instead of scoring the pool")
    parser.add_argument("--budget-tokens", type=int, default=1100)
    args = parser.parse_args()

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    tasks = json.loads(pathlib.Path(args.tasks).read_text())["tasks"]
    philosophy_text = pathlib.Path(args.philosophy).read_text()

    results_dir = pathlib.Path("results")
    results_dir.mkdir(exist_ok=True)

    if args.mutate:
        # Mutation mode: we first score the single candidate to collect its failures.
        candidate_path = pathlib.Path(args.mutate)
        candidate_text = candidate_path.read_text()
        score, failures = score_candidate(client, candidate_path.stem, candidate_text, tasks, results_dir)
        print(f"{candidate_path.name}: weighted fidelity {score:.1%}, {len(failures)} failed checks")

        if not failures:
            print("Nothing to fix; candidate is at full fidelity.")
            return

        revised = mutate_winner(client, candidate_text, failures, philosophy_text, args.budget_tokens)
        revised_path = results_dir / f"{candidate_path.stem}__gen_next.md"
        revised_path.write_text(revised)
        print(f"Wrote next generation to {revised_path}")
        return

    # Pool mode: score every candidate_*.md in the directory and report a leaderboard.
    leaderboard = []
    for candidate_path in sorted(pathlib.Path(args.candidates_dir).glob("candidate_*.md")):
        candidate_text = candidate_path.read_text()
        score, failures = score_candidate(client, candidate_path.stem, candidate_text, tasks, results_dir)
        leaderboard.append((score, candidate_path.name, len(failures)))
        print(f"scored {candidate_path.name}: {score:.1%} ({len(failures)} failed checks)")

    leaderboard.sort(reverse=True)
    print("\n=== LEADERBOARD (weighted behavioral fidelity) ===")
    for score, name, failure_count in leaderboard:
        print(f"{score:6.1%}  {name}  ({failure_count} failed checks)")
    print("\nNext step: python harness.py --mutate <winner> --budget-tokens <N>")


if __name__ == "__main__":
    main()
