import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import build_skill


class BuildSkillTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.output_dir = Path(self.temporary.name)
        self.skill_dir = build_skill.DEFAULT_SKILL_DIR

    def tearDown(self):
        self.temporary.cleanup()

    def test_every_cited_reference_exists(self):
        self.assertEqual(build_skill.find_missing_references(self.skill_dir), [])

    def test_claude_package_contains_skill_and_references(self):
        archive_path = build_skill.build_claude_package(self.skill_dir, self.output_dir)
        with zipfile.ZipFile(archive_path) as archive:
            names = set(archive.namelist())
        self.assertIn("licitacoes-servfaz/SKILL.md", names)
        expected_references = {f"licitacoes-servfaz/references/{path.name}" for path in (self.skill_dir / "references").glob("*.md")}
        self.assertTrue(expected_references <= names)

    def test_openwebui_files_are_self_contained(self):
        written = build_skill.build_openwebui_package(self.skill_dir, self.output_dir)
        self.assertEqual(len(written), 1 + len(build_skill.PHASE_BUNDLES))
        for path in written:
            content = path.read_text(encoding="utf-8")
            self.assertTrue(content.startswith("---\nname: licitacoes-servfaz"))
            self.assertIsNone(build_skill.REFERENCE_PATTERN.search(content), path.name)

    def test_full_openwebui_file_keeps_every_phase(self):
        full = build_skill.build_openwebui_package(self.skill_dir, self.output_dir)[0].read_text(encoding="utf-8")
        for phase_number in range(1, 6):
            self.assertIn(f"# Fase {phase_number} ", full)

    def test_main_rejects_missing_reference(self):
        broken_dir = self.output_dir / "quebrada"
        (broken_dir / "references").mkdir(parents=True)
        (broken_dir / "SKILL.md").write_text("---\nname: x\n---\nLeia `references/inexistente.md`.\n", encoding="utf-8")
        self.assertEqual(build_skill.main(["--skill-dir", str(broken_dir), "--output-dir", str(self.output_dir)]), 1)


if __name__ == "__main__":
    unittest.main()
