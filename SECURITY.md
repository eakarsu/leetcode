# Security policy

This is a non-executable educational source archive, not a deployed service. Treat every solution and binary shard as untrusted input. Do not bulk-run code, compile the whole tree, execute generated examples, concatenate or deserialize `xaa`–`xal`, or give CI write credentials. Consumers choose one file, review it, test it in an isolated resource-limited environment, and assume no correctness or side-channel guarantee.

`make check` verifies the pinned license, language inventory, workflow/write boundary, binary quarantine metadata/signature, safe launcher denial, and absence of high-confidence secret signatures. It does not prove the correctness or safety of hundreds of independent community solutions.

Report accidental credentials, malicious code, license/attribution issues, or private data privately to the fork custodian and relevant upstream maintainer. Revoke exposed credentials at their issuer, preserve evidence, and update the snapshot only through review. Any extracted product must name its own security-patching owner.
