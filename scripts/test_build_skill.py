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

    def write_skill(self, skill_text, references=None):
        skill_dir = self.output_dir / "skill-teste"
        (skill_dir / "references").mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(skill_text, encoding="utf-8")
        for relative_path, content in (references or {}).items():
            target = skill_dir / "references" / relative_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        return skill_dir

    def test_every_cited_reference_exists(self):
        self.assertEqual(build_skill.find_missing_references(self.skill_dir), [])

    def test_every_phase_has_instructions(self):
        for phase in ["fase-1-triagem", "fase-2-analise-edital", "fase-3-impugnacao", "fase-4-pcfp", "fase-5-recurso"]:
            self.assertTrue((self.skill_dir / "references" / phase / "instrucoes.md").is_file(), phase)

    def test_package_keeps_nested_references(self):
        archive_path = build_skill.build_package(self.skill_dir, self.output_dir)
        with zipfile.ZipFile(archive_path) as archive:
            names = set(archive.namelist())
        self.assertIn("licitacoes-servfaz/SKILL.md", names)
        self.assertIn("licitacoes-servfaz/references/estudo/edital/fontes.md", names)
        self.assertNotIn("licitacoes-servfaz/README.md", names)

    def test_nested_reference_resolves(self):
        skill_dir = self.write_skill("Leia `references/fase-1/instrucoes.md`.", {"fase-1/instrucoes.md": "# Fase 1\n"})
        self.assertEqual(build_skill.find_missing_references(skill_dir), [])

    def test_placeholder_path_is_not_a_reference(self):
        skill_dir = self.write_skill("Abra `references/estudo/<documento>/fontes.md`.")
        self.assertEqual(build_skill.find_missing_references(skill_dir), [])

    def test_oversized_document_is_reported(self):
        skill_dir = self.write_skill("# Skill\n", {"grande.md": "x" * 30})
        self.assertEqual(build_skill.find_oversized_documents(skill_dir, limit=20), [("references/grande.md", 30)])

    def test_main_rejects_missing_reference(self):
        skill_dir = self.write_skill("Leia `references/inexistente.md`.")
        self.assertEqual(build_skill.main(["--skill-dir", str(skill_dir), "--output-dir", str(self.output_dir)]), 1)


if __name__ == "__main__":
    unittest.main()
