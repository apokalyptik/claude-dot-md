# When Writing The Code — Counter-Instinct Rules

Principle: we place demands on ourselves, never on readers, callers, debuggers, or maintainers. Selfish code — easier to write, harder to understand — is bad even when tested and correct. Judge anything unlisted by the burden it puts downstream (assume the reader has plain text, grep, vim, 3am, and no IDE). Full reasoning: PHILOSOPHY.md.

Your instincts are wrong here in specific ways. Each rule overrides a default you will feel:

- You will reach for a ternary. Don't — ever. Write the if.
- You will reach for match. Use switch: explicit break or return in every case, fallthrough never, a default arm always (it reports failure).
- You will write `if ( $a || $b && ! ( $c || $d ) )`. Don't — in condition or assignment form. Name each condition as its own variable, then accumulate: default value, flat ifs, branch on the result.
- You will reach for array_map, array_filter, pipelines. Write the foreach; the extra obvious lines are the point. If the loop version genuinely buries its own logic in scaffolding, STOP: write both versions, show them, ask. Never just use the functional form.
- You will nest conditionals. Two levels deep means you skipped a guard or an accumulator. Guards: simple check-and-exit early returns, as early as knowable — exempt from length budgets while they stay simple.
- You will abbreviate names and write `process()`. Write the full sentence-word, globally greppable: `acme_sync_process_failures()`. Namespaces only for collision defense; even then, name as if they don't exist.
- You will DRY two similar loops. Ask first: would silent divergence be a bug? No → it's coincidence; leave both. Extract only for enforced consistency, or when a name fully replaces reading a body — and that name must stay the whole truth forever.
- You will accept the rich object the caller happens to hold. Take only what the function uses: charging takes card, amount, currency — never the Invoice. Domain objects belong only in the orchestration layer that guards and decomposes them.
- You will throw exceptions. Don't: return documented error values (docblock: "returns X, or null on error"; WP_Error where native; compound returns when failure carries detail). Check them immediately and adjacently. Catch third-party throws in the wrapper and convert. A throw taxes every layer above, forever.
- You will edit a failing test to make it pass. NEVER. It is either a regression (fix the code) or a contract change (present it; the human decides). Assert only what callers may rely on — post id 4 tests the auto-increment, not the insert.
- You will refactor code you weren't asked to touch. Don't. New code complies fully; modified lines comply; if your change lands inside a banned construct, unwind that construct only and cascade no further. Compliant code that reads unlike its legacy neighbors is correct — never "fix" it back.
- You will change a function other code calls. STOP: list the call sites, assess each, offer rename-all versus new-function. The human decides.
- You will want an exception to these rules. Two valid reasons only: no compliant alternative, or the exception genuinely reads better. Both trigger the same act: stop, write both versions as short examples, ask. Approvals are local — never precedent.

`??` is allowed for one thing: a visible default as the whole point of its own line — `$x = $input ?? 10;` — never embedded in a larger expression. One screen of working code is the target; two with a real reason; beyond that, stop and consider extraction — length never forces a split, only the question. Critique code, never authors. Context: long-lived PHP / WordPress code read for years by strangers.
