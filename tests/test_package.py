import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PackageTests(unittest.TestCase):
    def test_required_files_exist(self):
        for relative in [
            "SKILL.md",
            "README.md",
            "README.zh-CN.md",
            "LICENSE",
            "agents/openai.yaml",
            "references/assessment-framework.md",
            "references/output-templates.md",
            "references/evidence-and-safety.md",
            "references/research-and-learning.md",
            "docs/ARCHITECTURE.md",
            "docs/media/sunshine-workflow.svg",
            "scripts/learning_ledger.py",
            "examples/learning-event.example.json",
        ]:
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_skillhub_and_agent_frontmatter(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        frontmatter = text.split("---", 2)[1]
        for field in ["name", "license", "description", "metadata"]:
            self.assertRegex(frontmatter, rf"(?m)^{re.escape(field)}:")
        nested_skillhub = all(re.search(rf"(?m)^  {field}:", frontmatter) for field in [
            "skillhub-slug", "skillhub-display-name", "skillhub-summary"
        ])
        flat_skillhub = all(re.search(rf"(?m)^{field}:", frontmatter) for field in [
            "slug", "displayName", "version", "summary"
        ])
        self.assertTrue(nested_skillhub or flat_skillhub)

    def test_readme_local_links_resolve(self):
        for readme_name in ["README.md", "README.zh-CN.md"]:
            text = (ROOT / readme_name).read_text(encoding="utf-8")
            links = re.findall(r'(?:href|src)="([^"#][^"]*)"', text)
            markdown_links = re.findall(r"\[[^\]]+\]\(([^)#]+)(?:#[^)]+)?\)", text)
            for target in links + markdown_links:
                if target.startswith(("http://", "https://", "mailto:")):
                    continue
                self.assertTrue((ROOT / target).exists(), f"{readme_name}: {target}")

    def test_svg_assets_are_github_safe(self):
        svg_paths = list((ROOT / "docs" / "media").rglob("*.svg"))
        self.assertGreaterEqual(len(svg_paths), 6)
        for path in svg_paths:
            tree = ET.parse(path)
            for element in tree.iter():
                local_name = element.tag.rsplit("}", 1)[-1]
                self.assertNotIn(local_name, {"script", "foreignObject"}, str(path))
                for key, value in element.attrib.items():
                    self.assertFalse(key.lower().startswith("on"), str(path))
                    if key.rsplit("}", 1)[-1] == "href":
                        self.assertFalse(value.startswith(("http:", "https:", "data:")), str(path))

    def test_skill_declares_bilingual_research_and_explicit_learning(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Language / 语言", text)
        self.assertIn("Live research contract / 实时研究约定", text)
        self.assertIn("Explicit self-learning / 显式自学习", text)
        self.assertIn("references/research-and-learning.md", text)

    def test_no_scaffold_placeholders(self):
        placeholder = "TO" + "DO"
        for path in ROOT.rglob("*"):
            if path.is_file() and path.suffix in {".md", ".yaml", ".yml", ".py", ".json"}:
                self.assertNotIn(placeholder, path.read_text(encoding="utf-8"), str(path))


if __name__ == "__main__":
    unittest.main()
