import re
import struct
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = (
    REPO_ROOT
    / ".agents"
    / "skills"
    / "sunshineluyao-digital-nomad-wealth"
)


class PackageTests(unittest.TestCase):
    def test_required_files_exist(self):
        for relative in [
            "SKILL.md",
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
            "scripts/learning_ledger.py",
            "examples/learning-event.example.json",
        ]:
            self.assertTrue((SKILL_ROOT / relative).is_file(), relative)
        for relative in [
            "README.md",
            "README.zh-CN.md",
            "LICENSE",
            "PRIVACY.md",
            "SUPPORT.md",
            "CHANGELOG.md",
            "docs/ARCHITECTURE.md",
            "docs/ACCEPTANCE_TESTS.md",
            "docs/SKILLHUB_LISTING.md",
            "docs/media/sunshine-workflow.svg",
        ]:
            self.assertTrue((REPO_ROOT / relative).is_file(), relative)

    def test_single_canonical_discovery_location(self):
        self.assertTrue(SKILL_ROOT.is_dir())
        self.assertFalse((REPO_ROOT / "SKILL.md").exists())
        skill_files = list(REPO_ROOT.glob("**/SKILL.md"))
        self.assertEqual(skill_files, [SKILL_ROOT / "SKILL.md"])

    def test_skillhub_and_agent_frontmatter(self):
        text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        frontmatter = text.split("---", 2)[1]
        for field in ["name", "license", "description", "metadata"]:
            self.assertRegex(frontmatter, rf"(?m)^{re.escape(field)}:")
        for unsupported in ["slug", "displayName", "version", "summary"]:
            self.assertNotRegex(frontmatter, rf"(?m)^{re.escape(unsupported)}:")
        expected_slug = "sunshineluyao-digital-nomad-wealth"
        metadata_slug = re.search(r"(?m)^  skillhub-slug:\s*(\S+)", frontmatter)
        self.assertIsNotNone(metadata_slug)
        self.assertEqual(metadata_slug.group(1), expected_slug)
        name_match = re.search(r"(?m)^name:\s*(\S+)", frontmatter)
        self.assertIsNotNone(name_match)
        self.assertEqual(name_match.group(1), expected_slug)
        self.assertEqual(name_match.group(1), SKILL_ROOT.name)

    def test_readme_local_links_resolve(self):
        for readme_name in ["README.md", "README.zh-CN.md"]:
            text = (REPO_ROOT / readme_name).read_text(encoding="utf-8")
            links = re.findall(r'(?:href|src)="([^"#][^"]*)"', text)
            markdown_links = re.findall(r"\[[^\]]+\]\(([^)#]+)(?:#[^)]+)?\)", text)
            for target in links + markdown_links:
                if target.startswith(("http://", "https://", "mailto:")):
                    continue
                self.assertTrue((REPO_ROOT / target).exists(), f"{readme_name}: {target}")

    def test_svg_assets_are_github_safe(self):
        svg_paths = list((REPO_ROOT / "docs" / "media").rglob("*.svg"))
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
        text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Language / 语言", text)
        self.assertIn("Live research contract / 实时研究约定", text)
        self.assertIn("Explicit self-learning / 显式自学习", text)
        self.assertIn("references/research-and-learning.md", text)

    def test_marketplace_icons_have_expected_dimensions(self):
        for relative, expected in [
            ("assets/icon-128.png", (128, 128)),
            ("assets/icon-512.png", (512, 512)),
        ]:
            with (SKILL_ROOT / relative).open("rb") as stream:
                self.assertEqual(stream.read(8), b"\x89PNG\r\n\x1a\n")
                self.assertEqual(stream.read(4), b"\x00\x00\x00\r")
                self.assertEqual(stream.read(4), b"IHDR")
                width, height = struct.unpack(">II", stream.read(8))
            self.assertEqual((width, height), expected, relative)

    def test_privacy_and_release_material_are_explicit(self):
        privacy = (SKILL_ROOT / "PRIVACY.md").read_text(encoding="utf-8")
        listing = (REPO_ROOT / "docs" / "SKILLHUB_LISTING.md").read_text(encoding="utf-8")
        acceptance = (REPO_ROOT / "docs" / "ACCEPTANCE_TESTS.md").read_text(encoding="utf-8")
        for phrase in ["explicit permission", "does not train", "delete", "明确授权", "不训练", "删除"]:
            self.assertIn(phrase, privacy)
        self.assertIn("sunshineluyao-digital-nomad-wealth", listing)
        self.assertIn("8.", acceptance)

    def test_no_scaffold_placeholders(self):
        placeholder = "TO" + "DO"
        for path in REPO_ROOT.rglob("*"):
            if path.is_file() and path.suffix in {".md", ".yaml", ".yml", ".py", ".json"}:
                self.assertNotIn(placeholder, path.read_text(encoding="utf-8"), str(path))


if __name__ == "__main__":
    unittest.main()
