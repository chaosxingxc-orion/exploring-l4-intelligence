from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
CHECKS_DIR = SCRIPT_DIR.parent / "checks"
for path in (SCRIPT_DIR, CHECKS_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import ai_context_inventory
import sf_archive_candidates as archive
import sf_current_manifest
from ai_context_surface_check import TrustedRepoReader


def git(repo: Path, *arguments: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *arguments],
        cwd=repo,
        check=check,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


class ArchiveRepoFixture(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.repo = Path(self.temporary.name)
        git(self.repo, "init", "-q")
        git(self.repo, "config", "user.email", "archive-test@example.invalid")
        git(self.repo, "config", "user.name", "Archive Test")
        git(self.repo, "config", "core.autocrlf", "false")
        git(self.repo, "config", "core.eol", "lf")

        self.source = "wiki/survey/candidate.md"
        self.destination = "wiki/archive/working/campaign/candidate.md"
        self.write(self.source, b"candidate bytes\n")
        self.write(
            "wiki/survey/sf-audit-artifact-registry.json",
            self.registry_bytes([]),
        )
        for spec in sf_current_manifest.BASE_FILE_SPECS:
            path = self.repo.joinpath(*spec.path.split("/"))
            if not path.exists():
                self.write(spec.path, f"fixture {spec.role}\n".encode())
        self.write("wiki/Research-Objective.md", b"hot state\n")
        git(self.repo, "add", ".")
        self.restamp_current_manifest()
        git(self.repo, "commit", "-qm", "fixture")
        self.base_commit = git(self.repo, "rev-parse", "HEAD").stdout.decode().strip()
        blob = git(self.repo, "hash-object", "--", self.source).stdout.decode().strip()
        self.transitions = (
            {
                "source": self.source,
                "destination": self.destination,
                "git_blob": blob,
            },
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def write(self, relative: str, raw: bytes) -> None:
        path = self.repo.joinpath(*relative.split("/"))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)

    @staticmethod
    def registry_bytes(entries: list[dict]) -> bytes:
        return (json.dumps({"artifacts": entries}, indent=2) + "\n").encode()

    def current_manifest_document(self) -> dict:
        return json.loads(
            (self.repo / sf_current_manifest.OUTPUT_RELATIVE_PATH).read_text(
                encoding="utf-8"
            )
        )

    def restamp_current_manifest(self) -> None:
        inventory, read_blob = sf_current_manifest._git_release_context(self.repo)
        raw = sf_current_manifest.render_manifest(
            TrustedRepoReader(self.repo).read_bytes,
            inventory,
            read_blob,
        )
        self.write(sf_current_manifest.OUTPUT_RELATIVE_PATH, raw)
        git(self.repo, "add", "--", sf_current_manifest.OUTPUT_RELATIVE_PATH)

    def commit_rewrite(self, relative: str, raw: bytes) -> None:
        self.write(relative, raw)
        git(self.repo, "add", "--", relative)
        git(self.repo, "commit", "-qm", f"rewrite {Path(relative).name}")

    def assert_code(self, expected: str, operation) -> None:
        with self.assertRaises(archive.ArchiveSafetyError) as raised:
            operation()
        self.assertEqual(expected, raised.exception.code, str(raised.exception))


class ArchiveInventoryTests(unittest.TestCase):
    def test_default_transitions_are_the_shared_inventory_object(self) -> None:
        self.assertIs(ai_context_inventory.ARCHIVE_TRANSITIONS, archive.ARCHIVE_TRANSITIONS)
        self.assertEqual(7, len(archive.ARCHIVE_TRANSITIONS))

    def test_git_commands_reuse_the_cross_platform_worktree_prefix(self) -> None:
        self.assertIs(
            sf_current_manifest._git_command_prefix,
            archive.git_command_prefix,
        )

    def test_partial_and_both_states_fail_closed(self) -> None:
        transitions = (
            {"source": "wiki/survey/a.md", "destination": "wiki/archive/a.md", "git_blob": "1" * 40},
            {"source": "wiki/survey/b.md", "destination": "wiki/archive/b.md", "git_blob": "2" * 40},
        )
        for tracked in (
            {"wiki/survey/a.md": "1" * 40},
            {
                "wiki/survey/a.md": "1" * 40,
                "wiki/survey/b.md": "2" * 40,
                "wiki/archive/a.md": "1" * 40,
            },
        ):
            with self.subTest(tracked=tracked):
                with self.assertRaises(archive.ArchiveSafetyError) as raised:
                    archive.resolve_transition_state(transitions, tracked)
                self.assertEqual("archive-transition-incomplete", raised.exception.code)


class RepositoryArchiveIndexTests(unittest.TestCase):
    def test_production_archive_accepts_the_current_registered_prefix_anchor(self) -> None:
        repo = SCRIPT_DIR.parents[1]
        registry = json.loads(
            (repo / archive.REGISTRY_RELATIVE_PATH).read_text(encoding="utf-8")
        )["artifacts"]
        self.assertEqual(archive.REGISTRY_BASELINE_COUNT, len(registry))
        self.assertEqual(
            archive.REGISTRY_BASELINE_PREFIX_SHA256,
            archive.registry_prefix_sha256(
                registry, archive.REGISTRY_BASELINE_COUNT
            ),
        )
        self.assertEqual("post", archive.inspect_applied(repo).state)

    def test_cold_index_records_every_move_and_retained_exception(self) -> None:
        repo = SCRIPT_DIR.parents[1]
        index = (
            repo / "wiki/archive/working/system-first-stage1a/INDEX.md"
        ).read_text(encoding="utf-8")
        for transition in ai_context_inventory.ARCHIVE_TRANSITIONS:
            for field in ("source", "destination", "git_blob"):
                self.assertIn(transition[field], index)
        retained = (
            "wiki/survey/2026-07-15-sf-protocol-amendment-1.md",
            "wiki/survey/2026-07-16-sf-protocol-amendment-3.md",
            "wiki/survey/2026-07-16-sf-protocol-amendment-4.md",
            "wiki/survey/2026-07-16-sf-protocol-amendment-5.md",
            "wiki/survey/2026-07-17-sf-protocol-amendment-6.md",
            "wiki/survey/2026-07-17-sf-protocol-amendment-7.md",
            "wiki/survey/2026-07-18-sf-protocol-amendment-8.md",
        )
        for path in retained:
            self.assertIn(path, index)
        self.assertIn(
            "Commit intent: `chore(wiki): archive safe legacy amendments`",
            index,
        )

    def test_cold_index_rows_are_structurally_exact_and_swaps_fail(self) -> None:
        repo = SCRIPT_DIR.parents[1]
        raw = (
            repo / "wiki/archive/working/system-first-stage1a/INDEX.md"
        ).read_bytes()
        archive.validate_archive_index(raw, ai_context_inventory.ARCHIVE_TRANSITIONS)
        first, second = ai_context_inventory.ARCHIVE_TRANSITIONS[:2]
        mutated = raw.replace(first["source"].encode(), b"__SWAP__", 1)
        mutated = mutated.replace(second["source"].encode(), first["source"].encode(), 1)
        mutated = mutated.replace(b"__SWAP__", second["source"].encode(), 1)
        with self.assertRaises(archive.ArchiveSafetyError) as raised:
            archive.validate_archive_index(
                mutated, ai_context_inventory.ARCHIVE_TRANSITIONS
            )
        self.assertEqual("archive-index-invalid", raised.exception.code)


class ArchivePreMoveTests(ArchiveRepoFixture):
    def test_safe_pre_move_writes_exact_hash_object_plan_and_check_is_read_only(self) -> None:
        plan_path = self.repo / archive.PLAN_RELATIVE_PATH
        archive.write_plan(self.repo, self.transitions)
        document = json.loads(plan_path.read_text(encoding="utf-8"))
        self.assertEqual(
            [
                {
                    "source": self.source,
                    "destination": self.destination,
                    "pre_move_git_blob": self.transitions[0]["git_blob"],
                    "pre_move_git_mode": "100644",
                }
            ],
            document["transitions"],
        )
        self.assert_code(
            "archive-plan-untracked",
            lambda: archive.check_plan(self.repo, self.transitions),
        )
        git(self.repo, "add", "--", archive.PLAN_RELATIVE_PATH)
        before = plan_path.read_bytes()
        before_mtime = plan_path.stat().st_mtime_ns
        archive.check_plan(self.repo, self.transitions)
        self.assertEqual(before, plan_path.read_bytes())
        self.assertEqual(before_mtime, plan_path.stat().st_mtime_ns)

    def test_candidate_in_registry_or_invalid_current_manifest_fails_without_writing(self) -> None:
        candidate_blob = self.transitions[0]["git_blob"]
        current = self.current_manifest_document()
        current["files"].append(
            {
                "role": "forged_candidate",
                "path": self.source,
                "sha256": hashlib.sha256(b"candidate bytes\n").hexdigest(),
                "mutability": "frozen",
                "load_policy": "targeted",
            }
        )
        cases = (
            (
                "archive-source-registered-audit",
                "wiki/survey/sf-audit-artifact-registry.json",
                self.registry_bytes([{"path": self.source, "git_blob": candidate_blob}]),
            ),
            (
                "archive-current-manifest-invalid",
                "wiki/survey/current/manifest.json",
                (json.dumps(current, indent=2) + "\n").encode(),
            ),
        )
        for code, relative, raw in cases:
            with self.subTest(code=code):
                self.commit_rewrite(relative, raw)
                self.assert_code(
                    code,
                    lambda: archive.write_plan(self.repo, self.transitions),
                )
                self.assertFalse((self.repo / archive.PLAN_RELATIVE_PATH).exists())
                git(self.repo, "reset", "--hard", self.base_commit)

    def test_staged_registry_cannot_shorten_reorder_repath_or_repin_head(self) -> None:
        entries = []
        for name in ("first", "second"):
            path = f"wiki/audit/campaign/{name}.md"
            self.write(path, f"{name} audit\n".encode())
            git(self.repo, "add", "--", path)
            blob = git(self.repo, "hash-object", "--", path).stdout.decode().strip()
            entries.append({"path": path, "git_blob": blob})
        registry_path = "wiki/survey/sf-audit-artifact-registry.json"
        self.write(registry_path, self.registry_bytes(entries))
        git(self.repo, "add", "--", registry_path)
        git(self.repo, "commit", "-qm", "seed registry lineage")
        seeded_head = git(self.repo, "rev-parse", "HEAD").stdout.decode().strip()

        mutations = {
            "shorten": entries[:1],
            "reorder": list(reversed(entries)),
            "repath": [{**entries[0], "path": "wiki/audit/campaign/renamed.md"}, entries[1]],
            "repin": [{**entries[0], "git_blob": "0" * 40}, entries[1]],
        }
        for label, mutated in mutations.items():
            with self.subTest(label=label):
                git(self.repo, "reset", "--hard", seeded_head)
                self.write(registry_path, self.registry_bytes(mutated))
                git(self.repo, "add", "--", registry_path)
                self.assert_code(
                    "archive-registry-lineage-invalid",
                    lambda: archive.inspect_pre_move(self.repo, self.transitions),
                )

    def test_staged_registry_allows_exact_append_but_not_mode_drift(self) -> None:
        registry_path = "wiki/survey/sf-audit-artifact-registry.json"
        first = "wiki/audit/campaign/first.md"
        self.write(first, b"first audit\n")
        git(self.repo, "add", "--", first)
        first_blob = git(self.repo, "hash-object", "--", first).stdout.decode().strip()
        head_entries = [{"path": first, "git_blob": first_blob}]
        self.write(registry_path, self.registry_bytes(head_entries))
        git(self.repo, "add", "--", registry_path)
        git(self.repo, "commit", "-qm", "seed registry lineage")

        appended = "wiki/audit/campaign/appended.md"
        self.write(appended, b"appended audit\n")
        git(self.repo, "add", "--", appended)
        appended_blob = git(self.repo, "hash-object", "--", appended).stdout.decode().strip()
        self.write(
            registry_path,
            self.registry_bytes(
                [*head_entries, {"path": appended, "git_blob": appended_blob}]
            ),
        )
        git(self.repo, "add", "--", registry_path)
        self.assertEqual(
            "pre",
            archive.inspect_pre_move(self.repo, self.transitions).state,
        )

        git(self.repo, "update-index", "--chmod=+x", "--", registry_path)
        self.assert_code(
            "archive-registry-lineage-invalid",
            lambda: archive.inspect_pre_move(self.repo, self.transitions),
        )

    def test_hot_current_and_registered_audit_inbound_references_fail(self) -> None:
        registered = "wiki/audit/campaign/review.md"
        cases = (
            ("archive-inbound-active", "wiki/Research-Objective.md", []),
            ("archive-inbound-active", "wiki/survey/current/protocol.md", []),
            (
                "archive-inbound-registered-audit",
                registered,
                [{"path": registered, "git_blob": None}],
            ),
        )
        for code, referrer, registry in cases:
            with self.subTest(code=code, referrer=referrer):
                self.write(referrer, f"see `{self.source}`\n".encode())
                git(self.repo, "add", "--", referrer)
                if referrer == "wiki/survey/current/protocol.md":
                    self.restamp_current_manifest()
                if registry:
                    blob = git(self.repo, "hash-object", "--", referrer).stdout.decode().strip()
                    registry[0]["git_blob"] = blob
                    self.write(
                        "wiki/survey/sf-audit-artifact-registry.json",
                        self.registry_bytes(registry),
                    )
                    git(
                        self.repo,
                        "add",
                        "--",
                        "wiki/survey/sf-audit-artifact-registry.json",
                    )
                git(self.repo, "commit", "-qm", "add inbound reference")
                self.assert_code(
                    code,
                    lambda: archive.inspect_pre_move(self.repo, self.transitions),
                )
                git(self.repo, "reset", "--hard", self.base_commit)

    def test_reference_spellings_and_markdown_forms_are_detected_from_stage(self) -> None:
        upper_encoded = self.source.upper().replace("/", "%252f")
        relative = "survey/candidate.md"
        backslash = self.source.replace("/", "\\")
        cases = (
            f"plain {upper_encoded}\n",
            f"root /{self.source}\n",
            f"relative {relative}\n",
            f"inline `{backslash}`\n",
            f"[ref]: /{self.source}\n",
            f'<a href="/{self.source}">audit</a>\n',
            f"[link](/{self.source})\n",
            f"```text\n{self.source}\n```\n",
        )
        for text in cases:
            with self.subTest(text=text):
                self.commit_rewrite("wiki/Research-Objective.md", text.encode())
                self.assert_code(
                    "archive-inbound-active",
                    lambda: archive.inspect_pre_move(self.repo, self.transitions),
                )
                git(self.repo, "reset", "--hard", self.base_commit)

    def test_stage_only_and_worktree_only_references_fail_closed(self) -> None:
        hot = "wiki/Research-Objective.md"
        original = (self.repo / hot).read_bytes()
        reference = f"stage `{self.source}`\n".encode()

        self.write(hot, reference)
        git(self.repo, "add", "--", hot)
        self.write(hot, original)
        self.assert_code(
            "archive-input-dirty",
            lambda: archive.inspect_pre_move(self.repo, self.transitions),
        )

        git(self.repo, "reset", "--hard", "HEAD")
        self.write(hot, reference)
        self.assert_code(
            "archive-input-dirty",
            lambda: archive.inspect_pre_move(self.repo, self.transitions),
        )

    def test_invalid_candidate_encoding_and_controls_fail_closed(self) -> None:
        for raw in (
            b"wiki%ZZ/survey/candidate.md\n",
            f"{self.source}\x00\n".encode(),
        ):
            with self.subTest(raw=raw):
                self.commit_rewrite("wiki/Research-Objective.md", raw)
                self.assert_code(
                    "archive-reference-invalid",
                    lambda: archive.inspect_pre_move(self.repo, self.transitions),
                )
                git(self.repo, "reset", "--hard", self.base_commit)

    def test_missing_wrong_blob_and_dirty_source_fail_closed(self) -> None:
        cases = []
        git(self.repo, "rm", "-q", "--", self.source)
        cases.append(("archive-transition-incomplete", lambda: None))
        self.assert_code(
            cases[-1][0],
            lambda: archive.inspect_pre_move(self.repo, self.transitions),
        )
        git(self.repo, "reset", "--hard", "HEAD")

        wrong = ({**self.transitions[0], "git_blob": "0" * 40},)
        self.assert_code(
            "archive-transition-blob-mismatch",
            lambda: archive.inspect_pre_move(self.repo, wrong),
        )

        self.write(self.source, b"dirty candidate\n")
        self.assert_code(
            "archive-source-dirty",
            lambda: archive.inspect_pre_move(self.repo, self.transitions),
        )

    def test_staged_current_manifest_is_trusted_when_worktree_matches_index(self) -> None:
        self.write("wiki/survey/current/protocol.md", b"staged current protocol\n")
        git(self.repo, "add", "--", "wiki/survey/current/protocol.md")
        self.restamp_current_manifest()
        inspection = archive.inspect_pre_move(self.repo, self.transitions)
        self.assertEqual("pre", inspection.state)

    def test_current_manifest_must_equal_full_b4_rebuild_and_hash_closure(self) -> None:
        original = self.current_manifest_document()
        cases = {
            "empty": {**original, "files": []},
            "omitted": {**original, "files": original["files"][:-1]},
            "hash-tamper": {
                **original,
                "files": [
                    {**original["files"][0], "sha256": "0" * 64},
                    *original["files"][1:],
                ],
            },
        }
        for label, document in cases.items():
            with self.subTest(label=label):
                raw = (json.dumps(document, indent=2) + "\n").encode()
                self.write(sf_current_manifest.OUTPUT_RELATIVE_PATH, raw)
                git(self.repo, "add", "--", sf_current_manifest.OUTPUT_RELATIVE_PATH)
                self.assert_code(
                    "archive-current-manifest-invalid",
                    lambda: archive.inspect_pre_move(self.repo, self.transitions),
                )
                git(self.repo, "reset", "--hard", "HEAD")

    def test_source_mode_change_fails_before_plan(self) -> None:
        git(self.repo, "update-index", "--chmod=+x", "--", self.source)
        self.assert_code(
            "archive-source-mode-mismatch",
            lambda: archive.inspect_pre_move(self.repo, self.transitions),
        )

    def test_transition_read_paths_follow_only_complete_pre_or_post_state(self) -> None:
        self.assertEqual(
            (self.source,),
            archive.resolve_transition_read_paths(self.repo, self.transitions),
        )
        destination = self.repo.joinpath(*self.destination.split("/"))
        destination.parent.mkdir(parents=True, exist_ok=True)
        git(self.repo, "mv", "--", self.source, self.destination)
        self.assertEqual(
            (self.destination,),
            archive.resolve_transition_read_paths(self.repo, self.transitions),
        )


class ArchivePostMoveTests(ArchiveRepoFixture):
    def setUp(self) -> None:
        super().setUp()
        archive.write_plan(self.repo, self.transitions)
        git(self.repo, "add", "--", archive.PLAN_RELATIVE_PATH)
        git(self.repo, "commit", "-qm", "archive plan")

    def apply_move(self) -> None:
        destination = self.repo.joinpath(*self.destination.split("/"))
        destination.parent.mkdir(parents=True, exist_ok=True)
        git(self.repo, "mv", "--", self.source, self.destination)

    def test_complete_staged_move_with_identical_blob_passes(self) -> None:
        self.apply_move()
        archive.check_applied(self.repo, self.transitions)

    def test_plan_is_stage0_regular_exact_and_destination_mode_is_frozen(self) -> None:
        self.apply_move()
        git(self.repo, "update-index", "--chmod=+x", "--", self.destination)
        self.assert_code(
            "archive-destination-mode-mismatch",
            lambda: archive.check_applied(self.repo, self.transitions),
        )

        git(self.repo, "reset", "--hard", "HEAD")
        self.apply_move()
        plan = self.repo / archive.PLAN_RELATIVE_PATH
        original = plan.read_bytes()
        plan.write_bytes(original + b" \n")
        self.assert_code(
            "archive-plan-dirty",
            lambda: archive.check_applied(self.repo, self.transitions),
        )

        plan.write_bytes(original)
        git(self.repo, "update-index", "--chmod=+x", "--", archive.PLAN_RELATIVE_PATH)
        self.assert_code(
            "archive-plan-mode-invalid",
            lambda: archive.check_applied(self.repo, self.transitions),
        )

    def test_staged_exact_plan_schema_tamper_fails_closed(self) -> None:
        self.apply_move()
        plan_path = self.repo / archive.PLAN_RELATIVE_PATH
        document = json.loads(plan_path.read_text(encoding="utf-8"))
        document["transitions"][0]["pre_move_git_blob"] = "0" * 40
        plan_path.write_text(
            json.dumps(document, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        git(self.repo, "add", "--", archive.PLAN_RELATIVE_PATH)
        self.assert_code(
            "archive-plan-schema-invalid",
            lambda: archive.check_applied(self.repo, self.transitions),
        )

    def test_post_move_rejects_wrong_blob_restored_source_and_active_reference(self) -> None:
        self.apply_move()
        self.write(self.destination, b"changed after move\n")
        self.assert_code(
            "archive-destination-dirty",
            lambda: archive.check_applied(self.repo, self.transitions),
        )

        git(self.repo, "reset", "--hard", "HEAD")
        self.apply_move()
        self.write(self.source, b"untracked old path\n")
        self.assert_code(
            "archive-source-still-present",
            lambda: archive.check_applied(self.repo, self.transitions),
        )

        (self.repo / self.source).unlink()
        self.write(
            "wiki/survey/current/protocol.md",
            f"stale `{self.source}`\n".encode(),
        )
        git(self.repo, "add", "--", "wiki/survey/current/protocol.md")
        self.restamp_current_manifest()
        self.assert_code(
            "archive-inbound-active",
            lambda: archive.check_applied(self.repo, self.transitions),
        )


class ArchiveParserTests(unittest.TestCase):
    def test_index_parser_rejects_non_stage_zero_and_noncanonical_paths(self) -> None:
        for raw in (
            b"100644 " + b"1" * 40 + b" 1\tfile.md\0",
            b"100644 " + b"1" * 40 + b" 0\t../file.md\0",
        ):
            with self.subTest(raw=raw):
                with self.assertRaises(archive.ArchiveSafetyError) as raised:
                    archive.parse_index(raw)
                self.assertEqual("archive-git-index-invalid", raised.exception.code)


if __name__ == "__main__":
    unittest.main()
