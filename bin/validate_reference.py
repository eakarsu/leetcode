#!/usr/bin/env python3
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = ("c", "cpp", "csharp", "go", "java", "javascript", "kotlin", "python", "ruby", "rust", "scala", "swift", "typescript")
SECRET_PATTERNS = (
    re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(rb"AKIA[0-9A-Z]{16}"),
    re.compile(rb"\bsk-[A-Za-z0-9_-]{32,}\b"),
    re.compile(rb"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
)

def inspect():
    boundary = json.loads((ROOT / "REFERENCE_BOUNDARY.json").read_text())
    issues = []
    license_digest = hashlib.sha256((ROOT / "LICENSE").read_bytes()).hexdigest()
    if license_digest != boundary["license"]["sha256"]:
        issues.append("LICENSE digest mismatch")
    counts = {}
    for language in LANGUAGES:
        directory = ROOT / language
        counts[language] = sum(path.is_file() for path in directory.iterdir()) if directory.is_dir() else 0
        if not counts[language]: issues.append(f"missing or empty language directory: {language}")
    if boundary.get("application") is not False or boundary.get("executionSupported") is not False or boundary.get("deploymentSupported") is not False:
        issues.append("reference boundary must deny app execution and deployment")
    workflow_files = sorted((ROOT / ".github" / "workflows").glob("*.yml")) + sorted((ROOT / ".github" / "workflows").glob("*.yaml"))
    if [path.name for path in workflow_files] != ["reference-boundary.yml"]: issues.append("only reference-boundary.yml may execute")
    quarantined = boundary["binaryQuarantine"]
    sizes = {}
    for name in quarantined:
        path = ROOT / name
        if not path.is_file(): issues.append(f"missing quarantined shard {name}"); continue
        sizes[name] = path.stat().st_size
    if (ROOT / "xaa").read_bytes()[:8] != b"\x89HDF\r\n\x1a\n": issues.append("xaa HDF signature changed")
    scan_files = [ROOT / "README.md", ROOT / "PROVENANCE.md", ROOT / "start.sh"]
    scan_files.extend(path for language in LANGUAGES for path in (ROOT / language).iterdir() if path.is_file())
    for path in scan_files:
        data = path.read_bytes()
        if any(pattern.search(data) for pattern in SECRET_PATTERNS): issues.append(f"high-confidence secret signature: {path.relative_to(ROOT)}")
    return {"boundary": boundary, "languageFileCounts": counts, "solutionFileCount": sum(counts.values()), "quarantinedShardBytes": sum(sizes.values()), "licenseSha256": license_digest, "issues": issues}

if __name__ == "__main__":
    result = inspect(); print(json.dumps(result, indent=2, sort_keys=True)); raise SystemExit(bool(result["issues"]))
