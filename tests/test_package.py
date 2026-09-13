import re
import struct
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
            "PRIVACY.md",
            "SUPPORT.md",
            "CHANGELOG.md",
            "agents/openai.yaml",
            "assets/icon-128.png",
            "assets/icon-512.png",
            "references/assessment-framework.md",
            "references/output-templates.md",
            "references/evidence-and-safety.md",
            "references/research-and-learning.md",
            "docs/ARCHITECTURE.md",
            "docs/ACCEPTANCE_TESTS.md",
            "docs/SKILLHUB_LISTING.md",
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
        expected_slug = "sunshineluyao-digital-nomad-wealth"
        nested_match = re.search(r"(?m)^  skillhub-slug:\s*(\S+)", frontmatter)
        flat_match = re.search(r"(?m)^slug:\s*(\S+)", frontmatter)
        actual_slug = nested_match.group(1) if nested_match else flat_match.group(1)
        self.assertEqual(actual_slug, expected_slug)

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

    def test_marketplace_icons_have_expected_dimensions(self):
        for relative, expected in [
            ("assets/icon-128.png", (128, 128)),
            ("assets/icon-512.png", (512, 512)),
        ]:
            with (ROOT / relative).open("rb") as stream:
                self.assertEqual(stream.read(8), b"\x89PNG\r\n\x1a\n")
                self.assertEqual(stream.read(4), b"\x00\x00\x00\r")
                self.assertEqual(stream.read(4), b"IHDR")
                width, height = struct.unpack(">II", stream.read(8))
            self.assertEqual((width, height), expected, relative)

    def test_privacy_and_release_material_are_explicit(self):
        privacy = (ROOT / "PRIVACY.md").read_text(encoding="utf-8")
        listing = (ROOT / "docs" / "SKILLHUB_LISTING.md").read_text(encoding="utf-8")
        acceptance = (ROOT / "docs" / "ACCEPTANCE_TESTS.md").read_text(encoding="utf-8")
        for phrase in ["explicit permission", "does not train", "delete", "明确授权", "不训练", "删除"]:
            self.assertIn(phrase, privacy)
        self.assertIn("sunshineluyao-digital-nomad-wealth", listing)
        self.assertIn("8.", acceptance)

    def test_no_scaffold_placeholders(self):
        placeholder = "TO" + "DO"
        for path in ROOT.rglob("*"):
            if path.is_file() and path.suffix in {".md", ".yaml", ".yml", ".py", ".json"}:
                self.assertNotIn(placeholder, path.read_text(encoding="utf-8"), str(path))


if __name__ == "__main__":
    unittest.main()
