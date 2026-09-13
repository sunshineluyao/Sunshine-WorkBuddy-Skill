import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PackageTests(unittest.TestCase):
    def test_required_files_exist(self):
        for relative in [
            "SKILL.md",
            "README.md",
            "LICENSE",
            "agents/openai.yaml",
            "references/assessment-framework.md",
            "references/output-templates.md",
            "references/evidence-and-safety.md",
        ]:
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_skillhub_and_agent_frontmatter(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        frontmatter = text.split("---", 2)[1]
        for field in ["name", "license", "description", "metadata"]:
            self.assertRegex(frontmatter, rf"(?m)^{re.escape(field)}:")
        for value in [
            "skillhub-slug: sunshine-digital-nomad-wealth",
            "skillhub-display-name: 跨界数字游民财富导航",
            "skillhub-summary: 将跨界能力转化为全球机会、收入组合、证据资产与90天验证计划",
        ]:
            self.assertIn(value, frontmatter)

    def test_no_scaffold_placeholders(self):
        placeholder = "TO" + "DO"
        for path in ROOT.rglob("*"):
            if path.is_file() and path.suffix in {".md", ".yaml", ".yml", ".py", ".json"}:
                self.assertNotIn(placeholder, path.read_text(encoding="utf-8"), str(path))


if __name__ == "__main__":
    unittest.main()
