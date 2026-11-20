import unittest

from release_notes import filter_groups, group_commits, render


class ReleaseNotesTests(unittest.TestCase):
    def test_groups_conventional_commits(self):
        groups = group_commits(["feat(cli): add output", "fix: handle empty input"])
        self.assertEqual(groups["feat"], ["add output"])
        self.assertEqual(groups["fix"], ["handle empty input"])

    def test_unknown_commit_goes_to_other(self):
        self.assertEqual(group_commits(["update dependencies"])["other"], ["update dependencies"])

    def test_render_has_sections(self):
        output = render({"feat": ["add output"]}, "v1.0.0")
        self.assertIn("# v1.0.0", output)
        self.assertIn("## Features", output)

    def test_filter_groups_keeps_requested_kinds(self):
        groups = {"feat": ["add output"], "fix": ["handle input"]}
        self.assertEqual(filter_groups(groups, ["fix"]), {"fix": ["handle input"]})

    def test_filter_groups_without_filter_returns_all(self):
        groups = {"feat": ["add output"], "fix": ["handle input"]}
        self.assertEqual(filter_groups(groups, None), groups)


if __name__ == "__main__":
    unittest.main()
