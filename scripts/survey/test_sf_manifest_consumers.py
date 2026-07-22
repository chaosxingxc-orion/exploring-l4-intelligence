#!/usr/bin/env python3
"""Contract tests for current-manifest prose and release consumers."""

from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
SURVEY_SCRIPTS = REPO / "scripts" / "survey"


def load_module(name: str):
    path = SURVEY_SCRIPTS / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class ConsumerFixture:
    manifest_path = "wiki/survey/current/manifest.json"
    report_path = "docs/checks/release/report.json"
    release_path = "wiki/survey/current/tables/opening.md"
    prose_path = "wiki/survey/current/status.md"

    def __init__(self, root: Path, release_module):
        self.root = root
        self.release_module = release_module
        self.report = {
            "verdict": "PASS",
            "occupancy": {
                "policy_A": {
                    "is_reward_guided": {"n_paths": "6/11", "n_works": "5/8"},
                    "is_rq_sys_control_compatible": {
                        "n_paths": "5/11",
                        "n_works": "4/8",
                    },
                    "is_project_method_candidate": {
                        "n_paths": "0/11",
                        "n_works": "0/8",
                    },
                    "reward_guided_selection": {
                        "n_paths": "4/11",
                        "n_works": "3/8",
                    },
                    "strict_AND_reward_AND_pool_BY_selection_object(mechanism)": {
                        "trajectory": {"n_paths": "2/11", "n_works": "1/8"}
                    },
                }
            },
        }
        self.write_json(self.report_path, self.report)
        binding = {
            "source": self.report_path,
            "reward_guided": "6/11",
            "rq_sys_compatible": "5/11",
            "method_candidate": "0/11",
            "reward_guided_selection": "4/11",
            "trajectory_pool": "2/11",
        }
        headline = release_module.render_headline(self.report)
        self.write_text(
            self.release_path,
            f"<!-- release_binding: {json.dumps(binding)} -->\n"
            "<!-- generated_headline_begin -->\n"
            f"{headline}\n"
            "<!-- generated_headline_end -->\n",
        )
        self.write_text(self.prose_path, "Stage-1A scoped current state.\n")
        self.write_manifest()

    def target(self, relative: str) -> Path:
        return self.root.joinpath(*relative.split("/"))

    def write_text(self, relative: str, text: str):
        target = self.target(relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8", newline="\n")

    def write_json(self, relative: str, value):
        self.write_text(relative, json.dumps(value, ensure_ascii=False) + "\n")

    def entry(self, relative: str):
        raw = self.target(relative).read_bytes()
        return {
            "role": relative.replace("/", ":"),
            "path": relative,
            "sha256": hashlib.sha256(raw).hexdigest(),
            "mutability": "fixture",
            "load_policy": "targeted",
        }

    def manifest_document(self):
        paths = (self.report_path, self.release_path, self.prose_path)
        return {
            "schema": "sf-current-manifest-v1",
            "files": [self.entry(path) for path in paths],
            "release_bound_artifacts": [self.release_path],
            "prose_scan_paths": [self.prose_path],
        }

    def write_manifest(self, document=None):
        self.write_json(
            self.manifest_path,
            self.manifest_document() if document is None else document,
        )


class ManifestConsumerContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.current_manifest = load_module("sf_current_manifest")
        cls.release = load_module("sf_release_binding_check")
        cls.quantifier = load_module("sf_quantifier_scan")

    def fixture(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name) / "repo"
        root.mkdir()
        return ConsumerFixture(root, self.release)

    def run_main(self, module, argv, repo):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = module.main(argv, repo=repo)
        return code, output.getvalue()

    def test_git_repo_consumers_bind_stage0_blobs_not_crlf_worktree_bytes(self):
        fixture = self.fixture()
        for arguments in (
            ["init", "-q"],
            ["config", "user.email", "test@example.invalid"],
            ["config", "user.name", "Current Manifest Test"],
            ["config", "core.autocrlf", "false"],
            ["add", "."],
            ["commit", "-q", "-m", "fixture"],
        ):
            subprocess.run(
                ["git", *arguments],
                cwd=fixture.root,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

        prose = fixture.target(fixture.prose_path)
        prose.write_bytes(prose.read_bytes().replace(b"\n", b"\r\n"))
        loaded = self.current_manifest.load_consumer_manifest(
            fixture.root, fixture.manifest_path
        )
        self.assertEqual(
            b"Stage-1A scoped current state.\n",
            loaded.read_bytes(fixture.prose_path),
        )

        subprocess.run(
            ["git", "add", fixture.prose_path],
            cwd=fixture.root,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        with self.assertRaisesRegex(
            self.current_manifest.CurrentManifestError, "SHA-256 mismatch"
        ):
            self.current_manifest.load_consumer_manifest(
                fixture.root, fixture.manifest_path
            )

    def test_strict_manifest_schema_and_duplicate_paths_fail_closed(self):
        fixture = self.fixture()
        document = fixture.manifest_document()
        document["unexpected"] = True
        fixture.write_manifest(document)
        with self.assertRaisesRegex(
            self.current_manifest.CurrentManifestError, "manifest schema keys"
        ):
            self.current_manifest.load_consumer_manifest(
                fixture.root, fixture.manifest_path
            )

        raw = fixture.target(fixture.manifest_path).read_bytes()
        raw = raw.replace(b'{"schema":', b'{"schema":"wrong","schema":', 1)
        fixture.target(fixture.manifest_path).write_bytes(raw)
        with self.assertRaisesRegex(
            self.current_manifest.CurrentManifestError, "duplicate key"
        ):
            self.current_manifest.load_consumer_manifest(
                fixture.root, fixture.manifest_path
            )

        document = fixture.manifest_document()
        document["prose_scan_paths"].append(fixture.prose_path)
        fixture.write_manifest(document)
        with self.assertRaisesRegex(
            self.current_manifest.CurrentManifestError, "duplicates path"
        ):
            self.current_manifest.load_consumer_manifest(
                fixture.root, fixture.manifest_path
            )

        for key in ("release_bound_artifacts", "prose_scan_paths"):
            with self.subTest(empty_array=key):
                document = fixture.manifest_document()
                document[key] = []
                fixture.write_manifest(document)
                with self.assertRaisesRegex(
                    self.current_manifest.CurrentManifestError, "nonempty array"
                ):
                    self.current_manifest.load_consumer_manifest(
                        fixture.root, fixture.manifest_path
                    )

    def test_manifest_requires_canonical_nonarchive_hash_bound_existing_files(self):
        fixture = self.fixture()
        cases = []

        malformed = fixture.manifest_document()
        malformed["prose_scan_paths"] = ["wiki\\survey\\current\\status.md"]
        cases.append((malformed, "not canonical"))

        control = fixture.manifest_document()
        control["files"][-1] = dict(control["files"][-1])
        control["files"][-1]["path"] = "wiki/survey/current/sta\x00tus.md"
        control["prose_scan_paths"] = [control["files"][-1]["path"]]
        cases.append((control, "not canonical"))

        for unsafe in (
            "wiki/survey/current/sta\x7ftus.md",
            "wiki/survey/current/sta\x85tus.md",
            "wiki/survey/current/name:stream.md",
            "wiki/survey/current/trailing-space .md ",
            "wiki/survey/current/trailing-dot.",
            "wiki/survey/current/CON",
            "wiki/survey/current/con.txt",
            "wiki/survey/current/PrN.md",
            "wiki/survey/current/AUX.json",
            "wiki/survey/current/nul.log",
            "wiki/survey/current/COM1.md",
            "wiki/survey/current/com9.any",
            "wiki/survey/current/LPT1",
            "wiki/survey/current/lpt9.txt",
            "wiki/survey/current/CONIN$",
            "wiki/survey/current/conout$.txt",
            "wiki/survey/current/COM¹.md",
            "wiki/survey/current/lpt³.log",
            "wiki/survey/current/NUL .txt",
            "wiki/survey/current/CON .md",
            "wiki/survey/current/CONIN$ .json",
            "wiki/survey/current/CONOUT$ .x",
            "wiki/survey/current/COM1 .txt",
            "wiki/survey/current/COM¹ .txt",
            "wiki/survey/current/LPT³ .log",
            "wiki/survey/current/less<than.md",
            "wiki/survey/current/greater>than.md",
            'wiki/survey/current/double"quote.md',
            "wiki/survey/current/pipe|name.md",
            "wiki/survey/current/question?.md",
            "wiki/survey/current/star*.md",
            "wiki/survey/current/right-to-left-\u202e.md",
            "wiki/survey/current/line-\u2028separator.md",
            "wiki/survey/current/paragraph-\u2029separator.md",
            "wiki/survey/current/private-\ue000.md",
            "wiki/survey/current/unassigned-\u0378.md",
            "wiki/survey/current/e\u0301.md",
        ):
            document = fixture.manifest_document()
            document["files"][-1] = dict(document["files"][-1])
            document["files"][-1]["path"] = unsafe
            document["prose_scan_paths"] = [unsafe]
            cases.append((document, "not portable"))

        archive_path = "wiki/archive/system-first/old.md"
        fixture.write_text(archive_path, "old\n")
        archive = fixture.manifest_document()
        archive["files"].append(fixture.entry(archive_path))
        archive["prose_scan_paths"] = [archive_path]
        cases.append((archive, "archive path"))

        unknown = fixture.manifest_document()
        unknown["prose_scan_paths"] = ["wiki/survey/current/missing.md"]
        cases.append((unknown, "not present in files"))

        for document, message in cases:
            with self.subTest(message=message):
                fixture.write_manifest(document)
                with self.assertRaisesRegex(
                    self.current_manifest.CurrentManifestError, message
                ):
                    self.current_manifest.load_consumer_manifest(
                        fixture.root, fixture.manifest_path
                    )

        fixture.write_manifest()
        fixture.target(fixture.prose_path).write_text("changed\n", encoding="utf-8")
        with self.assertRaisesRegex(
            self.current_manifest.CurrentManifestError, "SHA-256 mismatch"
        ):
            self.current_manifest.load_consumer_manifest(
                fixture.root, fixture.manifest_path
            )

        fixture.target(fixture.prose_path).unlink()
        with self.assertRaisesRegex(
            self.current_manifest.CurrentManifestError, "missing"
        ):
            self.current_manifest.load_consumer_manifest(
                fixture.root, fixture.manifest_path
            )

    def test_portable_path_accepts_safe_nfc_names(self):
        safe_paths = (
            "wiki/survey/current/com10.md",
            "wiki/survey/current/lpt10.json",
            "wiki/survey/current/conifer.md",
            "wiki/survey/current/auxiliary.md",
            "wiki/survey/current/普通NFC中文路径.md",
            "wiki/survey/current/é.md",
        )
        for path in safe_paths:
            with self.subTest(path=path):
                self.assertEqual(
                    path, self.current_manifest.canonical_consumer_path(path)
                )

        for path in (
            "wiki/survey/current/surrogate-\ud800.md",
            "wiki/survey/current/   ",
        ):
            with self.subTest(path=repr(path)):
                with self.assertRaisesRegex(
                    self.current_manifest.CurrentManifestError, "not portable"
                ):
                    self.current_manifest.canonical_consumer_path(path)

    @unittest.skipUnless(hasattr(os, "symlink"), "symlink unavailable")
    def test_manifest_and_artifact_symlinks_are_not_followed(self):
        fixture = self.fixture()
        outside = fixture.root.parent / "outside.md"
        outside.write_text("outside\n", encoding="utf-8")
        artifact = fixture.target(fixture.prose_path)
        artifact.unlink()
        try:
            artifact.symlink_to(outside)
        except OSError as error:
            self.skipTest(f"symlink creation unavailable: {error}")
        with self.assertRaisesRegex(
            self.current_manifest.CurrentManifestError, "untrusted-repo-path"
        ):
            self.current_manifest.load_consumer_manifest(
                fixture.root, fixture.manifest_path
            )

        fixture = self.fixture()
        manifest = fixture.target(fixture.manifest_path)
        outside_manifest = fixture.root.parent / "outside-manifest.json"
        outside_manifest.write_bytes(manifest.read_bytes())
        manifest.unlink()
        manifest.symlink_to(outside_manifest)
        with self.assertRaisesRegex(
            self.current_manifest.CurrentManifestError, "untrusted-repo-path"
        ):
            self.current_manifest.load_consumer_manifest(
                fixture.root, fixture.manifest_path
            )

    def test_release_default_uses_manifest_and_missing_inputs_never_skip_green(self):
        fixture = self.fixture()
        code, output = self.run_main(self.release, [], fixture.root)
        self.assertEqual(0, code, output)
        self.assertIn("mode=current-manifest", output)
        self.assertNotIn("[skip]", output)

        fixture.target(fixture.release_path).unlink()
        code, output = self.run_main(self.release, [], fixture.root)
        self.assertEqual(1, code, output)
        self.assertIn("missing", output)
        self.assertNotIn("[skip]", output)

        fixture = self.fixture()
        fixture.target(fixture.manifest_path).unlink()
        code, output = self.run_main(self.release, [], fixture.root)
        self.assertEqual(1, code, output)
        self.assertIn("manifest", output)
        self.assertNotIn("[skip]", output)

    def test_release_binding_ignores_current_artifacts_without_legacy_occupancy_claims(self):
        fixture = self.fixture()
        document = fixture.manifest_document()
        document["release_bound_artifacts"].append(fixture.prose_path)
        fixture.write_manifest(document)

        code, output = self.run_main(self.release, [], fixture.root)
        self.assertEqual(0, code, output)
        self.assertIn("validated=1", output)
        self.assertIn("not-applicable=1", output)

    def test_release_rejects_stale_occupancy_and_hand_edited_headline(self):
        fixture = self.fixture()
        artifact = fixture.target(fixture.release_path)
        text = artifact.read_text(encoding="utf-8")
        artifact.write_text(text.replace('"6/11"', '"999/11"', 1), encoding="utf-8")
        fixture.write_manifest()
        code, output = self.run_main(self.release, [], fixture.root)
        self.assertEqual(1, code, output)
        self.assertIn("declared 999/11", output)

        fixture = self.fixture()
        artifact = fixture.target(fixture.release_path)
        text = artifact.read_text(encoding="utf-8")
        prefix, headline = text.split("<!-- generated_headline_begin -->", 1)
        artifact.write_text(
            prefix
            + "<!-- generated_headline_begin -->"
            + headline.replace("6/11", "99/11", 1),
            encoding="utf-8",
        )
        fixture.write_manifest()
        code, output = self.run_main(self.release, [], fixture.root)
        self.assertEqual(1, code, output)
        self.assertIn("generated headline block differs", output)

        fixture = self.fixture()
        artifact = fixture.target(fixture.release_path)
        text = artifact.read_text(encoding="utf-8")
        artifact.write_text(
            text.replace(
                '"reward_guided": "6/11"',
                '"reward_guided": "999/11", "reward_guided": "6/11"',
                1,
            ),
            encoding="utf-8",
        )
        fixture.write_manifest()
        code, output = self.run_main(self.release, [], fixture.root)
        self.assertEqual(1, code, output)
        self.assertIn("duplicate key", output)

    def test_current_release_artifact_has_closed_exact_syntax(self):
        mutations = {
            "source-only-no-headline": lambda text, fixture: (
                "<!-- release_binding: "
                + json.dumps({"source": fixture.report_path})
                + " -->\n"
            ),
            "two-bindings-second-stale": lambda text, fixture: text.replace(
                "<!-- generated_headline_begin -->",
                "<!-- release_binding: "
                + json.dumps(
                    {
                        "source": fixture.report_path,
                        "reward_guided": "999/11",
                        "rq_sys_compatible": "5/11",
                        "method_candidate": "0/11",
                        "reward_guided_selection": "4/11",
                        "trajectory_pool": "2/11",
                    }
                )
                + " -->\n<!-- generated_headline_begin -->",
                1,
            ),
            "two-headlines": lambda text, fixture: text
            + "<!-- generated_headline_begin -->\n"
            + self.release.render_headline(fixture.report)
            + "\n<!-- generated_headline_end -->\n",
            "dangling-marker": lambda text, fixture: text
            + "<!-- generated_headline_begin -->\n",
            "leading-body-space": lambda text, fixture: text.replace(
                "<!-- generated_headline_begin -->\n",
                "<!-- generated_headline_begin -->\n ",
                1,
            ),
            "trailing-body-space": lambda text, fixture: text.replace(
                "\n<!-- generated_headline_end -->",
                " \n<!-- generated_headline_end -->",
                1,
            ),
        }
        for name, mutate in mutations.items():
            with self.subTest(name=name):
                fixture = self.fixture()
                artifact = fixture.target(fixture.release_path)
                artifact.write_text(
                    mutate(artifact.read_text(encoding="utf-8"), fixture),
                    encoding="utf-8",
                )
                fixture.write_manifest()
                code, output = self.run_main(self.release, [], fixture.root)
                self.assertEqual(1, code, output)
                self.assertRegex(
                    output,
                    r"release_binding.*exact|generated headline.*exact|marker",
                )

    def test_legacy_compat_allows_zero_headline_but_keeps_exact_binding(self):
        fixture = self.fixture()
        text = fixture.target(fixture.release_path).read_text(encoding="utf-8")
        text = text.split("<!-- generated_headline_begin -->", 1)[0]
        cache = {fixture.report_path: fixture.report}
        self.assertEqual(
            [],
            self.release.check_artifact(
                text,
                "<legacy>",
                cache,
                mode="legacy-compat",
            ),
        )
        current_failures = self.release.check_artifact(
            text,
            "<current>",
            cache,
            mode="current-manifest",
        )
        self.assertTrue(
            any("generated headline" in failure for failure in current_failures)
        )

    def test_release_cli_rejects_manifest_and_legacy_conflict(self):
        with self.assertRaises(SystemExit) as raised:
            self.release.main(
                ["--manifest", "wiki/survey/current/manifest.json", "--legacy-regression"]
            )
        self.assertNotEqual(0, raised.exception.code)

    def test_release_cli_does_not_default_explicit_empty_manifest(self):
        fixture = self.fixture()
        for value in ("", "   "):
            with self.subTest(value=repr(value)):
                code, output = self.run_main(
                    self.release, ["--manifest", value], fixture.root
                )
                self.assertNotEqual(0, code, output)
                self.assertRegex(output, r"nonempty|not portable")

    def test_quantifier_defaults_to_manifest_and_positionals_remain_focused(self):
        fixture = self.fixture()
        code, output = self.run_main(self.quantifier, [], fixture.root)
        self.assertEqual(0, code, output)
        self.assertIn("scope=current-manifest", output)
        self.assertNotIn("[skip]", output)

        fixture.target(fixture.prose_path).unlink()
        code, output = self.run_main(self.quantifier, [], fixture.root)
        self.assertEqual(1, code, output)
        self.assertIn("missing", output)
        self.assertNotIn("[skip]", output)

        fixture = self.fixture()
        focused = "notes/focused.md"
        fixture.write_text(focused, "Stage-1A scoped.\n")
        fixture.target(fixture.manifest_path).unlink()
        code, output = self.run_main(self.quantifier, [focused], fixture.root)
        self.assertEqual(0, code, output)
        self.assertIn("PASS", output)
        self.assertIn("scope=focused-positional", output)

        missing = "notes/missing.md"
        code, output = self.run_main(self.quantifier, [missing], fixture.root)
        self.assertEqual(1, code, output)
        self.assertIn("missing", output)
        self.assertNotIn("[skip]", output)

    def test_quantifier_cli_rejects_explicit_manifest_with_positionals(self):
        fixture = self.fixture()
        with self.assertRaises(SystemExit) as raised:
            self.quantifier.main(
                ["--manifest", fixture.manifest_path, fixture.prose_path],
                repo=fixture.root,
            )
        self.assertNotEqual(0, raised.exception.code)

    def test_quantifier_cli_does_not_default_explicit_empty_manifest(self):
        fixture = self.fixture()
        for value in ("", "   "):
            with self.subTest(value=repr(value)):
                code, output = self.run_main(
                    self.quantifier, ["--manifest", value], fixture.root
                )
                self.assertNotEqual(0, code, output)
                self.assertRegex(output, r"nonempty|not portable")

    def test_quantifier_accepts_explicit_per_query_category_and_review_scope(self):
        scoped_lines = (
            "每查询 opensearch:totalResults 分页抓取至全量",
            "确定反例的主类目 cs.MM 唯一",
            "PRESS 独立复核唯一 MAJOR 的采纳",
        )
        for line in scoped_lines:
            with self.subTest(line=line):
                self.assertEqual([], self.quantifier.scan_text("<scoped>", line))
        self.assertTrue(
            self.quantifier.scan_text("<unscoped>", "这是全量且唯一的方法")
        )

    def test_default_current_arrays_have_no_legacy_amendment_or_opening_v4(self):
        document = json.loads((REPO / "wiki/survey/current/manifest.json").read_bytes())
        default_paths = (
            document["release_bound_artifacts"] + document["prose_scan_paths"]
        )
        self.assertFalse(
            any(
                "amendment-15" in path or "opening-tables-v4" in path
                for path in default_paths
            )
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
