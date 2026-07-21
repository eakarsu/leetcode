import json
import subprocess
import unittest
from pathlib import Path
from bin.validate_reference import inspect

ROOT = Path(__file__).resolve().parents[1]

class ReferenceBoundaryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.result = inspect()
    def test_retained_as_non_executable_upstream_reference(self):
        boundary = self.result["boundary"]; self.assertEqual(boundary["decision"], "retain-pinned-fork"); self.assertFalse(boundary["application"]); self.assertFalse(boundary["executionSupported"])
    def test_license_and_attribution_are_pinned(self):
        self.assertEqual(self.result["licenseSha256"], "a38883b60382c74837fce42753736e2efbb663c9458dee74b00e414558ae2c16"); self.assertEqual(self.result["boundary"]["license"]["identifier"], "MIT")
    def test_language_inventory_is_explicit(self):
        self.assertEqual(len(self.result["languageFileCounts"]), 13); self.assertEqual(self.result["solutionFileCount"], 1349)
    def test_unproven_binary_blobs_are_quarantined(self):
        self.assertEqual(len(self.result["boundary"]["binaryQuarantine"]), 12); self.assertEqual(self.result["quarantinedShardBytes"], 292_019_472)
    def test_boundary_scan_has_no_issues(self): self.assertEqual(self.result["issues"], [])
    def test_startup_is_denied(self):
        completed = subprocess.run([str(ROOT / "start.sh")], cwd=ROOT, capture_output=True, text=True, check=False); self.assertEqual(completed.returncode, 78); self.assertIn("not an executable application", completed.stderr)
    def test_extraction_requires_separate_ownership(self):
        text = (ROOT / "PRODUCT_EXTRACTION_CHECKLIST.md").read_text(); self.assertIn("separately owned product", text); self.assertIn("security owners", text)

if __name__ == "__main__": unittest.main()
