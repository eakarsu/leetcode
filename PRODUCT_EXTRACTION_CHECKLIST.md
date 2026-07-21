# Extraction checklist

Do not turn this archive itself into an app. For a separately owned product or library:

- Select exact source files and commits; preserve the MIT license/copyright and verify separate LeetCode/content/trademark rights.
- Name the product and security owners, users, acceptance criteria, supported language/toolchain, input bounds, and resource limits.
- Review algorithms for correctness, overflow, complexity, recursion/memory exhaustion, mutation, concurrency, Unicode, and adversarial input.
- Write independent tests and benchmarks; do not treat online-judge acceptance or README checkmarks as production evidence.
- Add a clean manifest/lockfile, isolated entry point, configuration contract, CI, signed release process, vulnerability patching, observability, rollback, and decommission policy.
- Exclude the quarantined binary shards and every unrelated solution from build/release context.
- Obtain security, legal/license, accessibility (if UI), operations, and representative-user approval before release.
