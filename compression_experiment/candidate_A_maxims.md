# When Writing The Code — Distilled

We place demands upon ourselves and do not place demands on others. Code made easier to write by means that make it harder to understand is selfish code — bad even when tested, functional, and correct.

Judge every construct by the demands it places downstream: on readers' tools (plain text, grep, vim at 3am — never assume an IDE), on mental decompilation, working memory, context switching, and skill; on debuggers needing visible intermediate state; on callers building above.

Control flow lives in statements, never expressions. Guards return early and discharge cases; mid-function decisions accumulate in a defaulted variable through flat ifs. Names are long, narrative, greppable, never abbreviated; a name — or a signature — must be the whole truth, for its whole life. Extract only when divergence between call sites would be a bug, or when a name can fully replace reading a body. Errors are documented return values; exceptions tax every layer above and are caught and converted at our boundary. Tests assert what callers may rely on, never what happens to be true; a failing test is a stop, not an inconvenience.

When no rule settles it, the principle settles it. When following a rule would burden the reader, or a discouraged pattern seems necessary or genuinely clearer: stop, write both versions, and ask. Approvals are local, never precedent. New code follows this fully; modified lines follow this; untouched neighbors are left alone. Critique code, never authors.

Context: long-lived PHP / WordPress-adjacent code read for years by strangers. Full reasoning: PHILOSOPHY.md.
