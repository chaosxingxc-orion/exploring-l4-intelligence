#!/usr/bin/env python3
"""Fail-closed AI context-surface and persistent-document routing oracle.

The evaluator is deliberately pure with respect to Git: callers supply the
tracked path inventory.  Only ``main`` shells out to obtain that inventory.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import subprocess
import sys
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit

from ai_context_inventory import ARCHIVE_TRANSITIONS


MANIFEST_RELATIVE_PATH = "docs/integrity/ai-context-manifest.json"
MANIFEST_SCHEMA = "ai-context-manifest-v1"
MANIFEST_KEYS = {
    "schema",
    "active_entries",
    "budgets_bytes",
    "legacy_cold_paths",
    "active_review_transaction",
}
ENTRY_KEYS = {"path", "class", "load_policy", "purpose", "sha256"}
SELF_ENTRY_KEYS = ENTRY_KEYS - {"sha256"}
LEGACY_KEYS = {"path", "class"}
LEGACY_CLASSES = {"AUDIT_LEGACY", "REGISTRY_LEGACY", "PENDING_ARCHIVE"}
COLD_ACTIVE_CLASSES = {
    "AUDIT",
    "ARCHIVE",
    "WORKBENCH",
    "EXPERIMENT",
    "AUDIT_LEGACY",
    "REGISTRY_LEGACY",
    "PENDING_ARCHIVE",
}
HOT_FILES = frozenset(
    {
        "AGENTS.md",
        "CLAUDE.md",
        "CONTRIBUTING.md",
        MANIFEST_RELATIVE_PATH,
        "wiki/Architecture.md",
        "wiki/AI-Collaboration.md",
        "wiki/Data-and-Assets.md",
        "wiki/Decision-Log.md",
        "wiki/Environment-and-Setup.md",
        "wiki/Experiment-Assets.md",
        "wiki/Home.md",
        "wiki/Inference-Engine-Choice.md",
        "wiki/Information-Boundary-Guard.md",
        "wiki/Onboarding.md",
        "wiki/Per-Work-Status.md",
        "wiki/Project-Thesis.md",
        "wiki/README.md",
        "wiki/Research-Methodology.md",
        "wiki/Research-Objective.md",
        "wiki/Working-Mode.md",
        "wiki/_Footer.md",
        "wiki/_Sidebar.md",
        "wiki/audit/system-first-stage1a/INDEX.md",
        "wiki/survey/README.md",
        "docs/checks/system-first-stage1a/evidence-v6/identity-taxonomy-v6-test.json",
        "docs/checks/system-first-stage1a/evidence-v6/identity-taxonomy-v6-test.nt.json",
        "docs/checks/system-first-stage1a/evidence-v6/identity-taxonomy-v6-test.posix.json",
        "docs/checks/system-first-stage1a/context-v1/current-package-check.json",
        "docs/checks/system-first-stage1a/context-v1/wiki-sync-dry-run-incident.json",
    }
)
PENDING_ARCHIVE_PATHS = frozenset(
    entry["source"] for entry in ARCHIVE_TRANSITIONS
)
AUDIT_NAME_RE = re.compile(
    r"(?:^|[-_.])(?:reviewer[-_.](?:submission|report)|submission|report|"
    r"(?:re)?review(?:er)?|response|correction|sign(?:[-_.]?off)|adjudication|"
    r"release[-_.]decision|proposal|amendment)(?:[-_.]|$)",
    re.IGNORECASE,
)
AMENDMENT_RE = re.compile(r"(?:^|[-_.])amendment(?:[-_.]|$)", re.IGNORECASE)
AMENDMENT_NUMBER_RE = re.compile(
    r"(?:^|[-_.])amendment[-_.]?(\d+)(?:[-_.]|$)", re.IGNORECASE
)
NUMBERED_ITERATION_RE = re.compile(
    r"(?:^|[-_.])(?:amendment|correction)[-_.]?(\d+)(?:[-_.]|$)",
    re.IGNORECASE,
)
EPOCH_DIRECTORY_RE = re.compile(r"epoch-([1-9]\d*)\Z")
AUDIT_ITERATION_KIND_RE = re.compile(
    r"(?:^|[-_.])(?P<kind>amendment|correction)(?:[-_.]|$)", re.IGNORECASE
)
AUDIT_ITERATION_PATH_RE = re.compile(
    r"\Awiki/audit/(?P<campaign>[A-Za-z0-9][A-Za-z0-9._-]*)/"
    r"epoch-(?P<epoch>[1-9]\d*)/"
    r"(?P<round>[A-Za-z0-9][A-Za-z0-9._-]*)/"
    r"(?:[A-Za-z0-9][A-Za-z0-9._-]*[-_.])?"
    r"(?P<kind>amendment|correction)-(?P<ordinal>[1-9]\d*)\.md\Z",
    re.IGNORECASE,
)
CONSOLIDATION_RECEIPT_PATH_RE = re.compile(
    r"\Awiki/audit/(?P<campaign>[A-Za-z0-9][A-Za-z0-9._-]*)/"
    r"epoch-(?P<epoch>[1-9]\d*)/consolidation-receipt\.json\Z"
)
FIXED_AUDIT_ITERATION_EXCEPTIONS = frozenset(
    {
        "wiki/audit/system-first-stage1a/round-12/"
        "stage1a-readiness-correction.md"
    }
)
AUDIT_ITERATION_SCHEMA = "ai-context-audit-iteration-v1"
AUDIT_ITERATION_KEYS = {
    "schema",
    "campaign",
    "epoch",
    "ordinal",
    "kind",
    "effective_spec",
    "effective_spec_version",
    "effective_spec_sha256",
}
EFFECTIVE_PROTOCOL_PATH = "wiki/survey/current/protocol.md"
# The Stage-1 survey package closed on 2026-08-03: the protocol carrier moved
# to the archive with its bytes preserved. Immutable audit records keep the
# historical spec id above; live existence/byte checks resolve through this
# prefix relocation.
CURRENT_LAYER_RELOCATION = (
    "wiki/survey/current/",
    "wiki/archive/working/system-first-survey-current/",
)


def resolve_effective_spec(spec: str) -> str:
    """Map a historically recorded current-layer spec path to its archive home."""

    old_prefix, new_prefix = CURRENT_LAYER_RELOCATION
    if spec.startswith(old_prefix):
        return new_prefix + spec[len(old_prefix) :]
    return spec
CONSOLIDATION_RECEIPT_SCHEMA = "ai-context-consolidation-receipt-v1"
CONSOLIDATION_RECEIPT_KEYS = {
    "schema",
    "campaign",
    "epoch",
    "effective_spec",
    "effective_spec_version",
    "effective_spec_sha256",
}
INLINE_LINK_RE = re.compile(
    r"!?\[[^\]\n]*\]\(\s*(?:<([^>\n]+)>|([^\s)]+))(?:\s+[^)]*)?\s*\)"
)
REFERENCE_DEFINITION_RE = re.compile(
    r"^[ ]{0,3}\[((?:\\.|[^\[\]\n])+)\]:[ \t]*"
    r"(?:<([^>\n]*)>|([^ \t\n]+))"
    r"(?:[ \t]+(?:\"[^\"\n]*\"|'[^'\n]*'|\([^\)\n]*\)))?[ \t]*$"
)
REFERENCE_DEFINITION_HEAD_RE = re.compile(
    r"^[ ]{0,3}\[((?:\\.|[^\[\]\n])+)\]:[ \t]*$"
)
REFERENCE_DESTINATION_RE = re.compile(
    r"^[ ]{1,3}(?:<([^>\n]*)>|([^ \t\n]+))"
    r"(?:[ \t]+(?:\"[^\"\n]*\"|'[^'\n]*'|\([^\)\n]*\)))?[ \t]*$"
)
FENCE_OPEN_RE = re.compile(r"^[ ]{0,3}(?:(`{3,})[^`\n]*|(~{3,})[^\n]*)$")
HTML_TAG_RE = re.compile(r"<[A-Za-z][^<>\n]*>")
HTML_ATTRIBUTE_RE = re.compile(
    r"\b(?:href|src)[ \t]*=[ \t]*(?:\"([^\"\n]*)\"|'([^'\n]*)'|([^\s\"'=<>`]+))",
    re.IGNORECASE,
)
HTML_COMMENT_RE = re.compile(r"<!--[\s\S]*?(?:-->|\Z)")
HTML_PRE_BLOCK_RE = re.compile(
    r"<pre\b[^>]*>[\s\S]*?(?:</pre[ \t]*>|\Z)", re.IGNORECASE
)
RAW_AUDIT_URL_RE = re.compile(
    r"(?<![A-Za-z0-9_])(?:https?://[^\s<>\[\]{}\"']+|"
    r"//[^\s<>\[\]{}\"']+|/wiki/audit/[^\s<>\[\]{}\"']+)",
    re.IGNORECASE,
)
LIST_MARKER_RE = re.compile(r"^[ ]{0,3}(?:[-+*]|\d+[.)])[ \t]+")
RESIDUAL_PERCENT_ENCODING_RE = re.compile(r"%[0-9A-Fa-f]{2}")
SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")
CLIENT_NORMALIZATIONS = (
    ("# AGENTS.md", "# CLIENT-GUIDE.md"),
    ("# CLAUDE.md", "# CLIENT-GUIDE.md"),
    (
        "This file provides guidance to Codex (Codex.ai/code) "
        "when working with code in this repository.",
        "This file provides guidance to CLIENT when working with code in this repository.",
    ),
    (
        "This file provides guidance to Claude Code (claude.ai/code) "
        "when working with code in this repository.",
        "This file provides guidance to CLIENT when working with code in this repository.",
    ),
    (
        "Installed via the Windows Codex plugin marketplace (see `docs/setup.md`):",
        "Installed via the Windows CLIENT plugin marketplace (see `docs/setup.md`):",
    ),
    (
        "Installed via the Windows Claude Code plugin marketplace (see `docs/setup.md`):",
        "Installed via the Windows CLIENT plugin marketplace (see `docs/setup.md`):",
    ),
)
AGENT_GUIDE_CLIENTS = {
    "AGENTS": {
        "h1": "# AGENTS.md",
        "description": (
            "This file provides guidance to Codex (Codex.ai/code) "
            "when working with code in this repository."
        ),
        "marketplace": (
            "Installed via the Windows Codex plugin marketplace (see `docs/setup.md`):"
        ),
    },
    "CLAUDE": {
        "h1": "# CLAUDE.md",
        "description": (
            "This file provides guidance to Claude Code (claude.ai/code) "
            "when working with code in this repository."
        ),
        "marketplace": (
            "Installed via the Windows Claude Code plugin marketplace (see `docs/setup.md`):"
        ),
    },
}


class ContextSurfaceError(ValueError):
    """Controlled policy/schema error."""


class TrustedRepoReader:
    """Read regular repository files without following in-tree symlinks."""

    def __init__(self, repo):
        try:
            self.root = Path(repo).resolve(strict=True)
        except OSError as exc:
            raise ContextSurfaceError(_failure("repo-root-invalid", str(exc))) from exc
        if not self.root.is_dir():
            raise ContextSurfaceError(
                _failure("repo-root-invalid", f"not a directory: {self.root}")
            )

    @staticmethod
    def _identity(metadata):
        return (metadata.st_dev, metadata.st_ino, stat.S_IFMT(metadata.st_mode))

    def read_bytes(self, relative_path: str) -> bytes:
        path = _canonical_path(relative_path, "repository read path")
        candidate = self.root.joinpath(*PurePosixPath(path).parts)
        component_metadata = []
        current = self.root
        try:
            for part in PurePosixPath(path).parts:
                current = current / part
                metadata = os.lstat(current)
                if stat.S_ISLNK(metadata.st_mode):
                    raise ContextSurfaceError(
                        _failure("untrusted-repo-path", f"{path}: symlink component {part}")
                    )
                component_metadata.append((current, metadata))
            resolved = candidate.resolve(strict=True)
            try:
                resolved.relative_to(self.root)
            except ValueError as exc:
                raise ContextSurfaceError(
                    _failure("untrusted-repo-path", f"{path}: resolves outside repository")
                ) from exc
            flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
            descriptor = os.open(candidate, flags)
            try:
                before = os.fstat(descriptor)
                if not stat.S_ISREG(before.st_mode):
                    raise ContextSurfaceError(
                        _failure("untrusted-repo-path", f"{path}: not a regular file")
                    )
                with os.fdopen(descriptor, "rb", closefd=False) as stream:
                    raw = stream.read()
                after = os.fstat(descriptor)
            finally:
                os.close(descriptor)
            if (
                self._identity(before) != self._identity(after)
                or before.st_size != after.st_size
                or getattr(before, "st_mtime_ns", None) != getattr(after, "st_mtime_ns", None)
            ):
                raise ContextSurfaceError(
                    _failure("repo-read-raced", f"{path}: file changed while being read")
                )
            for component, original in component_metadata:
                current_metadata = os.lstat(component)
                if stat.S_ISLNK(current_metadata.st_mode) or self._identity(
                    original
                ) != self._identity(current_metadata):
                    raise ContextSurfaceError(
                        _failure("repo-read-raced", f"{path}: path changed while being read")
                    )
            if len(raw) != after.st_size:
                raise ContextSurfaceError(
                    _failure("repo-read-raced", f"{path}: short or expanding read")
                )
            return raw
        except ContextSurfaceError:
            raise
        except FileNotFoundError as exc:
            raise ContextSurfaceError(_failure("repo-path-missing", path)) from exc
        except OSError as exc:
            raise ContextSurfaceError(
                _failure("repo-read-failed", f"{path}: {exc}")
            ) from exc


def _failure(code: str, detail: str) -> str:
    return f"{code}: {detail}"


def _canonical_path(value: object, label: str = "path") -> str:
    if not isinstance(value, str):
        raise ContextSurfaceError(_failure("invalid-path", f"{label} must be a string"))
    if not value or value in {".", ".."}:
        raise ContextSurfaceError(_failure("invalid-path", f"{label} is empty or dot-only"))
    if "\\" in value:
        raise ContextSurfaceError(_failure("invalid-path", f"{label} uses a backslash: {value!r}"))
    if value.startswith("/") or re.match(r"^[A-Za-z]:", value):
        raise ContextSurfaceError(_failure("invalid-path", f"{label} is absolute: {value!r}"))
    path = PurePosixPath(value)
    if any(part in {"", ".", ".."} for part in path.parts):
        raise ContextSurfaceError(
            _failure("invalid-path", f"{label} is not canonical repo-relative POSIX: {value!r}")
        )
    canonical = path.as_posix()
    if canonical != value:
        raise ContextSurfaceError(
            _failure("invalid-path", f"{label} is not canonical repo-relative POSIX: {value!r}")
        )
    return canonical


def _legacy_map(legacy_cold_paths: object) -> dict[str, str]:
    if not isinstance(legacy_cold_paths, list):
        raise ContextSurfaceError(
            _failure("manifest-schema-invalid", "legacy_cold_paths must be a list")
        )
    result: dict[str, str] = {}
    for index, entry in enumerate(legacy_cold_paths):
        if not isinstance(entry, dict) or set(entry) != LEGACY_KEYS:
            raise ContextSurfaceError(
                _failure(
                    "manifest-schema-invalid",
                    f"legacy_cold_paths[{index}] must have exact keys {sorted(LEGACY_KEYS)}",
                )
            )
        path = _canonical_path(entry["path"], f"legacy_cold_paths[{index}].path")
        path_class = entry["class"]
        if not isinstance(path_class, str) or path_class not in LEGACY_CLASSES:
            raise ContextSurfaceError(
                _failure(
                    "manifest-schema-invalid",
                    f"legacy_cold_paths[{index}].class is invalid: {path_class!r}",
                )
            )
        expected_class = _expected_legacy_class(path)
        if path_class != expected_class:
            raise ContextSurfaceError(
                _failure(
                    "legacy-class-mismatch",
                    f"{path}: declared {path_class!r}, expected {expected_class!r}",
                )
            )
        if path in result:
            raise ContextSurfaceError(_failure("duplicate-path", f"legacy path {path}"))
        result[path] = path_class
    return result


def classify_path(path, legacy_cold_paths):
    """Classify one canonical repository path using the policy precedence."""

    canonical = _canonical_path(path)
    legacy = _legacy_map(legacy_cold_paths)
    if canonical in HOT_FILES:
        return "HOT"
    if canonical.startswith("wiki/survey/registry/") or canonical.startswith(
        "wiki/survey/sidecars/"
    ):
        return "REGISTRY"
    if canonical.startswith("wiki/audit/"):
        return "AUDIT"
    if canonical.startswith("wiki/archive/"):
        return "ARCHIVE"
    if canonical.startswith("wiki/survey/workbench/"):
        return "WORKBENCH"
    if canonical.startswith("wiki/experiments/"):
        return "EXPERIMENT"
    if canonical in legacy:
        return legacy[canonical]
    return "UNCLASSIFIED"


def _expected_legacy_class(path: str) -> str:
    if path in PENDING_ARCHIVE_PATHS:
        return "PENDING_ARCHIVE"
    basename = PurePosixPath(path).name
    if path.lower().endswith(".md") and AUDIT_NAME_RE.search(basename):
        return "AUDIT_LEGACY"
    return "REGISTRY_LEGACY"


def normalize_agent_guide(text):
    """Normalize only the three intentional Codex/Claude guide differences."""

    if not isinstance(text, str):
        raise TypeError("agent guide must be text")
    plain_lines = text.splitlines()
    if not plain_lines:
        raise ContextSurfaceError(_failure("agent-guide-shape-invalid", "empty guide"))
    matching_clients = [
        name
        for name, shape in AGENT_GUIDE_CLIENTS.items()
        if plain_lines[0] == shape["h1"]
    ]
    if len(matching_clients) != 1:
        raise ContextSurfaceError(
            _failure("agent-guide-shape-invalid", "client H1 must be exact on line 1")
        )
    client = matching_clients[0]
    shape = AGENT_GUIDE_CLIENTS[client]
    for foreign_client, foreign_shape in AGENT_GUIDE_CLIENTS.items():
        if foreign_client == client:
            continue
        for field in ("h1", "description", "marketplace"):
            if foreign_shape[field] in plain_lines:
                raise ContextSurfaceError(
                    _failure(
                        "agent-guide-shape-invalid",
                        f"{client} guide contains foreign {foreign_client} {field}",
                    )
                )
    for field in ("h1", "description", "marketplace"):
        if plain_lines.count(shape[field]) != 1:
            raise ContextSurfaceError(
                _failure(
                    "agent-guide-shape-invalid",
                    f"{client} {field} must occur exactly once",
                )
            )
    first_paragraph_line = next(
        (line for line in plain_lines[1:] if line.strip()), None
    )
    if first_paragraph_line != shape["description"]:
        raise ContextSurfaceError(
            _failure(
                "agent-guide-shape-invalid",
                f"{client} description must be the first paragraph",
            )
        )
    if plain_lines.count("## Research skills") != 1:
        raise ContextSurfaceError(
            _failure(
                "agent-guide-shape-invalid",
                "Research skills heading must occur exactly once",
            )
        )
    research_index = plain_lines.index("## Research skills")
    next_heading = next(
        (
            index
            for index in range(research_index + 1, len(plain_lines))
            if plain_lines[index].startswith("## ")
        ),
        len(plain_lines),
    )
    first_research_line = next(
        (
            line
            for line in plain_lines[research_index + 1 : next_heading]
            if line.strip()
        ),
        None,
    )
    if first_research_line != shape["marketplace"]:
        raise ContextSurfaceError(
            _failure(
                "agent-guide-shape-invalid",
                f"{client} marketplace line must open Research skills",
            )
        )
    lines = text.splitlines(keepends=True)
    normalized: list[str] = []
    for line in lines:
        ending = ""
        body = line
        if line.endswith("\r\n"):
            body, ending = line[:-2], "\r\n"
        elif line.endswith("\n") or line.endswith("\r"):
            body, ending = line[:-1], line[-1]
        for source, target in CLIENT_NORMALIZATIONS:
            if body == source:
                body = target
                break
        normalized.append(body + ending)
    return "".join(normalized)


POLICY_TABLE_HEADERS = (
    "类型",
    "必须位置",
    "谁读取",
    "默认加载",
    "权威性/可变性",
    "进入条件",
    "搬运/退出条件",
)
POLICY_ROLE_ORDER = (
    "HOT",
    "REGISTRY",
    "AUDIT",
    "ARCHIVE",
    "WORKBENCH",
    "Engineering spec",
    "Engineering plan",
    "Study repository registry",
    "Study experiment index",
    "Check report",
    "Executable rule",
    "Ephemeral scratch",
)
POLICY_ROLE_SEMANTICS = {
    "HOT": (
        ("AGENTS.md", "wiki/Research-Objective.md", "wiki/Project-Thesis.md"),
        ("每个新会话", "前三项", "按需"),
        ("仅前三项",),
        ("当前事实", "supersede-in-place"),
        ("owner 裁决", "当前阶段", "阻塞项"),
        ("原位替换", "冷索引", "不得日期版本化"),
    ),
    "REGISTRY": (
        ("wiki/survey/registry/", "wiki/survey/sidecars/"),
        ("论文核验", "编码", "写作"),
        ("否",),
        ("append-only", "supersede"),
        ("FETCH", "精读", "canonical ID", "claim"),
        ("跨 campaign 保留", "不得复制", "不删记录"),
    ),
    "AUDIT": (
        ("wiki/audit/<campaign>/<round-id>/", "INDEX.md"),
        ("reviewer", "审计者", "精确取证"),
        ("否",),
        ("immutable", "append-only"),
        ("submission", "report", "response", "correction", "sign-off"),
        ("永不移动/改写", "campaign index"),
    ),
    "ARCHIVE": (
        ("wiki/archive/<knowledge-layer>/<campaign>/",),
        ("历史", "复现"),
        ("否",),
        ("immutable",),
        ("闭合", "不再有活跃依赖"),
        ("永久冷存", "不回迁"),
    ),
    "WORKBENCH": (
        ("wiki/survey/workbench/<campaign>/",),
        ("当前探索者",),
        ("否",),
        ("可变工作知识", "不得承载完成声明"),
        ("探索", "未被接受"),
        ("整编进 HOT/REGISTRY", "归档", "scratch 不提交"),
    ),
    "Engineering spec": (
        ("docs/superpowers/specs/",),
        ("实现者", "reviewer"),
        ("否",),
        ("工程设计", "Git review"),
        ("多步骤工程改动",),
        ("Git 历史保留", "research current page 不依赖"),
    ),
    "Engineering plan": (
        ("docs/superpowers/plans/",),
        ("实现者",),
        ("否",),
        ("checkbox 可变",),
        ("已批准设计",),
        ("停止作为 current research pointer", "Git 保存"),
    ),
    "Study repository registry": (
        ("studies/README.md", "studies/registry.json"),
        ("owner", "实现者", "CI"),
        ("否", "工程任务定向"),
        ("伞仓跟踪", "语义命名独立 Git 仓"),
        ("OWNER_GO_AND_EXECUTION_CONTRACT",),
        ("候选编号不得成为 repo 名", "不得建空仓"),
    ),
    "Study experiment index": (
        ("wiki/experiments/<study-slug>/README.md", "wiki/Experiment-Assets.md"),
        ("owner", "实现者", "reviewer"),
        ("否", "study 定向"),
        ("Wiki 管理实验状态与资产图",),
        ("study 已登记", "实验合同"),
        ("稳定当前页", "release/audit bytes 不回写"),
    ),
    "Check report": (
        ("docs/checks/<campaign>/<release-id>/",),
        ("门禁工具", "核验者"),
        ("否",),
        ("release 引用后 immutable",),
        ("可重复检查", "平台/版本"),
        ("新 release 新目录", "禁止跨平台"),
    ),
    "Executable rule": (
        ("scripts/",),
        ("CI", "操作者", "reviewer"),
        ("否", "执行而非通读"),
        ("代码生命周期", "测试先行"),
        ("机械验证",),
        ("同步测试", "不维护第二套实现"),
    ),
    "Ephemeral scratch": (
        ("Not committed",),
        ("当前会话",),
        ("否",),
        ("无权威性",),
        ("临时推理", "草稿", "一次性输出"),
        ("提炼", "provenance", "删除/过期"),
    ),
}


def _markdown_table_cells(line: str) -> list[str] | None:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return None
    return [cell.strip() for cell in stripped[1:-1].split("|")]


def _policy_invalid(detail: str) -> str:
    return _failure("collaboration-policy-invalid", detail)


def validate_collaboration_policy(text: str) -> list[str]:
    """Validate the canonical policy structurally and semantically."""

    failures: list[str] = []
    if not isinstance(text, str):
        return [_policy_invalid("policy must be UTF-8 text")]
    section_match = re.search(
        r"^## 2\. 文档类型与唯一位置\s*$([\s\S]*?)(?=^## 3\.)",
        text,
        re.MULTILINE,
    )
    if section_match is None:
        return [_policy_invalid("missing exact §2 placement section")]
    table_lines = [
        line for line in section_match.group(1).splitlines() if line.strip().startswith("|")
    ]
    parsed = [_markdown_table_cells(line) for line in table_lines]
    if len(parsed) != len(POLICY_ROLE_ORDER) + 2 or any(row is None for row in parsed):
        failures.append(
            _policy_invalid(
                "§2 must contain one header, divider, and "
                f"{len(POLICY_ROLE_ORDER)} rows"
            )
        )
    else:
        header = tuple(parsed[0])
        if header != POLICY_TABLE_HEADERS:
            failures.append(_policy_invalid(f"§2 headers differ: {header!r}"))
        divider = parsed[1]
        if len(divider) != 7 or any(re.fullmatch(r":?-{3,}:?", cell) is None for cell in divider):
            failures.append(_policy_invalid("§2 divider must have seven Markdown columns"))
        rows = parsed[2:]
        roles = tuple(re.sub(r"^\*\*|\*\*$", "", row[0]) for row in rows)
        if roles != POLICY_ROLE_ORDER:
            failures.append(_policy_invalid(f"§2 role order differs: {roles!r}"))
        for role, row in zip(roles, rows):
            if len(row) != 7:
                failures.append(_policy_invalid(f"{role}: expected seven columns"))
                continue
            semantics = POLICY_ROLE_SEMANTICS.get(role)
            if semantics is None:
                continue
            for column_offset, tokens in enumerate(semantics, start=1):
                cell = row[column_offset]
                missing = [token for token in tokens if token not in cell]
                if missing:
                    failures.append(
                        _policy_invalid(
                            f"{role}/{POLICY_TABLE_HEADERS[column_offset]} missing {missing!r}"
                        )
                    )
    if any(token in section_match.group(1) for token in ("允许覆写", "可改写", "可以移动并覆盖")):
        failures.append(_policy_invalid("§2 reverses immutable/exit semantics"))

    lifecycle_match = re.search(
        r"^## 3\. 六步生命周期\s*$([\s\S]*?)(?=^## 4\.)",
        text,
        re.MULTILINE,
    )
    if lifecycle_match is None:
        failures.append(_policy_invalid("missing exact §3 lifecycle"))
    else:
        lifecycle = re.findall(
            r"^(\d+)\. \*\*([^*]+)\*\* — ",
            lifecycle_match.group(1),
            re.MULTILINE,
        )
        expected = tuple(
            (str(index), name)
            for index, name in enumerate(
                (
                    "Capture",
                    "Classify",
                    "Work",
                    "Consolidate",
                    "Release / Audit",
                    "Archive / Expire",
                ),
                start=1,
            )
        )
        if tuple(lifecycle) != expected:
            failures.append(_policy_invalid(f"lifecycle order differs: {lifecycle!r}"))
        lifecycle_tokens = (
            "结论、推理摘要、目的链、provenance、失效条件",
            "指定唯一角色",
            "CURRENT 稳定文件中",
            "更新 current manifest",
            "AUDIT 永久路径",
            "先提炼、再清 manifest/引用、最后搬运",
        )
        for token in lifecycle_tokens:
            if token not in lifecycle_match.group(1):
                failures.append(_policy_invalid(f"lifecycle missing semantic {token!r}"))

    trigger_match = re.search(
        r"^## 4\. 强制整编与搬运时点\s*$([\s\S]*?)(?=^### 搬运前安全门)",
        text,
        re.MULTILINE,
    )
    if trigger_match is None:
        failures.append(_policy_invalid("missing exact §4 trigger section"))
    else:
        trigger_text = trigger_match.group(1)
        if "以下任一事件先发生就立即 Consolidate：" not in trigger_text:
            failures.append(_policy_invalid("triggers must direct immediate Consolidate"))
        bullets = [
            line[2:].strip()
            for line in trigger_text.splitlines()
            if line.startswith("- ")
        ]
        if len(bullets) != 6:
            failures.append(_policy_invalid(f"expected exactly six triggers, found {len(bullets)}"))
        trigger_semantics = (
            ("第三次", "amendment", "correction"),
            ("超过 context budget",),
            ("reviewer Gate MAJOR", "executable contract"),
            ("handoff ambiguity",),
            ("stage/release boundary",),
            ("competing active claims",),
        )
        for index, tokens in enumerate(trigger_semantics):
            if index >= len(bullets) or any(token not in bullets[index] for token in tokens):
                failures.append(_policy_invalid(f"trigger {index + 1} semantics differ"))
        for token in (
            "第三次修正必须立即折叠",
            "第四次修正禁止新增",
            "ordinal",
            "consolidation epoch",
            "consolidation-receipt.json",
            "schema=`ai-context-audit-iteration-v1`",
            "Artifact 与 receipt 都必须进入 audit registry",
            "epoch 从 1 连续递增",
            "ordinal 唯一且连续",
            "先 commit receipt、append 注册",
            "registry prefix count/hash anchor",
            "wiki/survey/current/protocol.md",
        ):
            if token not in trigger_text:
                failures.append(_policy_invalid(f"consolidation rule missing {token!r}"))

    move_match = re.search(
        r"^### 搬运前安全门（强制）\s*$([\s\S]*?)(?=^## 5\.)",
        text,
        re.MULTILINE,
    )
    if move_match is None:
        failures.append(_policy_invalid("missing exact stage-0 move gate"))
    else:
        move_items = re.findall(r"^([1-5])\. (.+)$", move_match.group(1), re.MULTILINE)
        if tuple(number for number, _ in move_items) != ("1", "2", "3", "4", "5"):
            failures.append(_policy_invalid("move gate must contain five ordered items"))
        for token in (
            "stage-0",
            "regular-file path、mode 与 Git blob",
            "audit registry",
            "current manifest",
            "inbound reference",
            "active script",
            "partial/both-path 状态 fail closed",
            "git mv",
            "mode/blob 相同",
        ):
            if token not in move_match.group(1):
                failures.append(_policy_invalid(f"move gate missing {token!r}"))
    return failures


def _strict_json_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ContextSurfaceError(_failure("manifest-json-invalid", f"duplicate key {key!r}"))
        result[key] = value
    return result


def _reject_nonfinite(value: str):
    raise ContextSurfaceError(_failure("manifest-json-invalid", f"non-finite number {value}"))


def loads_json_strict(raw: bytes, label: str = "JSON"):
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ContextSurfaceError(
            _failure("manifest-json-invalid", f"invalid UTF-8: {exc}")
        ) from exc
    try:
        return json.loads(
            text,
            object_pairs_hook=_strict_json_object,
            parse_constant=_reject_nonfinite,
        )
    except ContextSurfaceError:
        raise
    except (json.JSONDecodeError, ValueError) as exc:
        raise ContextSurfaceError(_failure("manifest-json-invalid", str(exc))) from exc


def load_json_strict(path: Path):
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise ContextSurfaceError(_failure("manifest-missing", f"{path}: {exc}")) from exc
    return loads_json_strict(raw, str(path))


def _join_repo(repo: Path, relative_path: str) -> Path:
    return repo.joinpath(*PurePosixPath(relative_path).parts)


def _normalize_link_target(source_path: str, raw_target: str) -> str | None:
    target = raw_target.strip()
    for _ in range(5):
        try:
            decoded = unquote(target, errors="strict")
        except UnicodeDecodeError as exc:
            raise ContextSurfaceError(
                _failure(
                    "invalid-link-path",
                    f"invalid percent encoding: {source_path} -> {raw_target}",
                )
            ) from exc
        if decoded == target:
            break
        target = decoded
    if RESIDUAL_PERCENT_ENCODING_RE.search(target):
        raise ContextSurfaceError(
            _failure("invalid-link-path", f"residual encoding: {source_path} -> {raw_target}")
        )
    if not target or target.startswith("#"):
        return None
    absolute_url = False
    if target.startswith("//"):
        absolute_url = True
        target = urlsplit(f"https:{target}").path
    elif re.match(r"^https?://", target, re.IGNORECASE):
        absolute_url = True
        target = urlsplit(target).path
    elif re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", target):
        return None
    else:
        target = target.split("#", 1)[0].split("?", 1)[0]
    if target.startswith("/wiki/"):
        target = target[1:]
    elif absolute_url:
        audit_segment = re.search(r"/wiki/audit(?:/|$)", target)
        if audit_segment is None:
            return None
        target = target[audit_segment.start() + 1 :]
    if not target:
        return None
    if "\\" in target or target.startswith("/") or re.match(r"^[A-Za-z]:", target):
        raise ContextSurfaceError(_failure("invalid-link-path", f"{source_path} -> {raw_target}"))
    target_path = PurePosixPath(target)
    if target.startswith(("wiki/", "docs/", "scripts/")) or target in HOT_FILES:
        components: list[str] = []
    else:
        components = list(PurePosixPath(source_path).parent.parts)
    for part in target_path.parts:
        if part in {"", "."}:
            continue
        if part == "..":
            if not components:
                raise ContextSurfaceError(
                    _failure(
                        "invalid-link-path",
                        f"link escapes repository: {source_path} -> {raw_target}",
                    )
                )
            components.pop()
        else:
            components.append(part)
    if not components:
        return None
    return _canonical_path(PurePosixPath(*components).as_posix(), "link target")


def _is_direct_audit_round_link(path: str) -> bool:
    parts = PurePosixPath(path).parts
    if len(parts) < 4 or parts[:2] != ("wiki", "audit"):
        return False
    return not (len(parts) == 4 and parts[-1] == "INDEX.md")


def _blank_except_newlines(text: str) -> str:
    return "".join(character if character in "\r\n" else " " for character in text)


def _backtick_is_escaped(text: str, position: int) -> bool:
    backslashes = 0
    cursor = position - 1
    while cursor >= 0 and text[cursor] == "\\":
        backslashes += 1
        cursor -= 1
    return backslashes % 2 == 1


def _mask_inline_code_spans(text: str) -> str:
    characters = list(text)
    cursor = 0
    while cursor < len(text):
        opening = text.find("`", cursor)
        if opening < 0:
            break
        if _backtick_is_escaped(text, opening):
            cursor = opening + 1
            continue
        opening_end = opening
        while opening_end < len(text) and text[opening_end] == "`":
            opening_end += 1
        delimiter_length = opening_end - opening
        search = opening_end
        closing_end = None
        while search < len(text):
            closing = text.find("`", search)
            if closing < 0:
                break
            if _backtick_is_escaped(text, closing):
                search = closing + 1
                continue
            run_end = closing
            while run_end < len(text) and text[run_end] == "`":
                run_end += 1
            if run_end - closing == delimiter_length:
                closing_end = run_end
                break
            search = run_end
        if closing_end is None:
            cursor = opening_end
            continue
        for index in range(opening, closing_end):
            if characters[index] not in "\r\n":
                characters[index] = " "
        cursor = closing_end
    return "".join(characters)


def _mask_markdown_code(text: str) -> str:
    """Mask Markdown/HTML code and comments while preserving line structure."""

    masked_lines: list[str] = []
    fence_character: str | None = None
    fence_length = 0
    in_list = False
    for line in text.splitlines(keepends=True):
        content = line.rstrip("\r\n")
        if fence_character is not None:
            close = re.match(
                rf"^[ ]{{0,3}}{re.escape(fence_character)}{{{fence_length},}}[ \t]*$",
                content,
            )
            masked_lines.append(_blank_except_newlines(line))
            if close:
                fence_character = None
                fence_length = 0
            continue
        opener = FENCE_OPEN_RE.match(content)
        if opener:
            marker = opener.group(1) or opener.group(2)
            fence_character = marker[0]
            fence_length = len(marker)
            masked_lines.append(_blank_except_newlines(line))
            continue
        if LIST_MARKER_RE.match(content):
            in_list = True
            masked_lines.append(line)
            continue
        if re.match(r"^(?: {4}| {0,3}\t)", content):
            spaces = len(content) - len(content.lstrip(" "))
            if in_list and 4 <= spaces < 8 and not content.startswith("\t"):
                masked_lines.append(line)
            else:
                masked_lines.append(_blank_except_newlines(line))
            continue
        if content.strip():
            in_list = False
        masked_lines.append(line)
    masked = "".join(masked_lines)
    masked = HTML_COMMENT_RE.sub(lambda match: _blank_except_newlines(match.group()), masked)
    masked = HTML_PRE_BLOCK_RE.sub(
        lambda match: _blank_except_newlines(match.group()), masked
    )
    return _mask_inline_code_spans(masked)


def _mask_spans(text: str, spans) -> str:
    characters = list(text)
    for start, end in spans:
        for index in range(start, end):
            if characters[index] not in "\r\n":
                characters[index] = " "
    return "".join(characters)


def _link_targets(text: str):
    """Yield Markdown, finite HTML-attribute, and standalone URL destinations."""

    masked_spans: list[tuple[int, int]] = []
    for match in INLINE_LINK_RE.finditer(text):
        masked_spans.append(match.span())
        yield match.group(1) or match.group(2)

    yield from _reference_definition_targets(text)

    for tag in HTML_TAG_RE.finditer(text):
        masked_spans.append(tag.span())
        for attribute in HTML_ATTRIBUTE_RE.finditer(tag.group()):
            yield attribute.group(1) or attribute.group(2) or attribute.group(3)

    raw_scan = _mask_spans(text, masked_spans)
    for match in RAW_AUDIT_URL_RE.finditer(raw_scan):
        yield match.group().rstrip(".,;:!?")


def _reference_definition_targets(text: str):
    """Yield valid one- or two-line Markdown reference destinations.

    Definitions are scanned even when no usage is present.  That conservative
    choice prevents a later reference usage from silently activating a cold
    audit dependency.  The caller supplies shared code-masked text; footnote
    definitions are not link definitions for this policy and are ignored.
    """

    lines = text.splitlines()
    for index, line in enumerate(lines):
        definition = REFERENCE_DEFINITION_RE.match(line)
        if definition:
            raw_label = definition.group(1)
            if raw_label.strip() and not raw_label.startswith("^"):
                yield (
                    definition.group(2)
                    if definition.group(2) is not None
                    else definition.group(3)
                )
            continue
        head = REFERENCE_DEFINITION_HEAD_RE.match(line)
        if not head or index + 1 >= len(lines):
            continue
        raw_label = head.group(1)
        if not raw_label.strip() or raw_label.startswith("^"):
            continue
        destination = REFERENCE_DESTINATION_RE.match(lines[index + 1])
        if destination:
            yield (
                destination.group(1)
                if destination.group(1) is not None
                else destination.group(2)
            )


def _validate_manifest_shape(manifest: object, failures: list[str]):
    if not isinstance(manifest, dict):
        failures.append(_failure("manifest-schema-invalid", "manifest must be an object"))
        return {}, [], {}, [], None
    if set(manifest) != MANIFEST_KEYS:
        failures.append(
            _failure(
                "manifest-schema-invalid",
                f"top-level keys must be exactly {sorted(MANIFEST_KEYS)}",
            )
        )
    if manifest.get("schema") != MANIFEST_SCHEMA:
        failures.append(
            _failure("manifest-schema-invalid", f"schema must be {MANIFEST_SCHEMA!r}")
        )
    active = manifest.get("active_entries", [])
    budgets = manifest.get("budgets_bytes", {})
    legacy = manifest.get("legacy_cold_paths", [])
    active_review = manifest.get("active_review_transaction")
    if not isinstance(active, list):
        failures.append(_failure("manifest-schema-invalid", "active_entries must be a list"))
        active = []
    if not isinstance(budgets, dict):
        failures.append(_failure("manifest-schema-invalid", "budgets_bytes must be an object"))
        budgets = {}
    if active_review is not None and not isinstance(active_review, str):
        failures.append(
            _failure("manifest-schema-invalid", "active_review_transaction must be null or a path")
        )
        active_review = None
    return manifest, active, budgets, legacy, active_review


def _front_matter_protocol_version(raw: bytes, path: str) -> int | None:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return None
    match = re.search(
        r"^protocol_version:\s*(?:\"([1-9]\d*)\"|([1-9]\d*))\s*$",
        text,
        re.MULTILINE,
    )
    if match is None:
        return None
    return int(match.group(1) or match.group(2))


def _parse_audit_iteration_front_matter(raw: bytes, path: str) -> dict[str, object]:
    """Parse the exact flat front matter for one registered epoch iteration."""

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ContextSurfaceError(
            _failure("audit-iteration-metadata-invalid", f"{path}: invalid UTF-8: {exc}")
        ) from exc
    if "\r" in text or not text.startswith("---\n"):
        raise ContextSurfaceError(
            _failure(
                "audit-iteration-metadata-invalid",
                f"{path}: front matter must start with LF-only ---",
            )
        )
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ContextSurfaceError(
            _failure("audit-iteration-metadata-invalid", f"{path}: unclosed front matter")
        )
    values: dict[str, str] = {}
    for line in text[4:end].split("\n"):
        if not line or ": " not in line:
            raise ContextSurfaceError(
                _failure(
                    "audit-iteration-metadata-invalid",
                    f"{path}: front matter must use one 'key: value' per line",
                )
            )
        key, value = line.split(": ", 1)
        if not key or not value or key in values:
            raise ContextSurfaceError(
                _failure(
                    "audit-iteration-metadata-invalid",
                    f"{path}: empty or duplicate front-matter field {key!r}",
                )
            )
        values[key] = value
    if set(values) != AUDIT_ITERATION_KEYS:
        raise ContextSurfaceError(
            _failure(
                "audit-iteration-metadata-invalid",
                f"{path}: exact fields must be {sorted(AUDIT_ITERATION_KEYS)}",
            )
        )
    if values["schema"] != AUDIT_ITERATION_SCHEMA:
        raise ContextSurfaceError(
            _failure(
                "audit-iteration-metadata-invalid",
                f"{path}: schema must be {AUDIT_ITERATION_SCHEMA}",
            )
        )
    parsed: dict[str, object] = dict(values)
    for field in ("epoch", "ordinal", "effective_spec_version"):
        value = values[field]
        if re.fullmatch(r"[1-9]\d*", value) is None:
            raise ContextSurfaceError(
                _failure(
                    "audit-iteration-metadata-invalid",
                    f"{path}: {field} must be a positive canonical integer",
                )
            )
        parsed[field] = int(value)
    if values["kind"] not in {"amendment", "correction"}:
        raise ContextSurfaceError(
            _failure(
                "audit-iteration-metadata-invalid",
                f"{path}: kind must be amendment or correction",
            )
        )
    try:
        parsed["effective_spec"] = _canonical_path(
            values["effective_spec"], f"{path}.effective_spec"
        )
    except ContextSurfaceError as exc:
        raise ContextSurfaceError(
            _failure("audit-iteration-metadata-invalid", str(exc))
        ) from exc
    if SHA256_RE.fullmatch(values["effective_spec_sha256"]) is None:
        raise ContextSurfaceError(
            _failure(
                "audit-iteration-metadata-invalid",
                f"{path}: effective_spec_sha256 must be lowercase SHA-256",
            )
        )
    return parsed


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def validate_audit_epoch_state(
    manifest: object,
    tracked_paths: object,
    registered_blobs: object,
    read_bytes,
) -> list[str]:
    """Pure registered-graph validator for numbered audit iteration epochs."""

    failures: list[str] = []
    if not isinstance(tracked_paths, (list, tuple, set, frozenset)):
        return [_failure("audit-epoch-state-invalid", "tracked_paths must be explicit")]
    if not isinstance(registered_blobs, dict):
        return [_failure("audit-epoch-state-invalid", "registered_blobs must be a map")]
    if not callable(read_bytes):
        return [_failure("audit-epoch-state-invalid", "read_bytes must be callable")]

    tracked: set[str] = set()
    for index, raw_path in enumerate(tracked_paths):
        try:
            path = _canonical_path(raw_path, f"tracked_paths[{index}]")
        except ContextSurfaceError as exc:
            failures.append(str(exc))
            continue
        if path in tracked:
            failures.append(_failure("duplicate-path", f"tracked path {path}"))
        tracked.add(path)

    registered: dict[str, str] = {}
    for raw_path, blob in registered_blobs.items():
        try:
            path = _canonical_path(raw_path, "registered audit path")
        except ContextSurfaceError as exc:
            failures.append(str(exc))
            continue
        if path in registered:
            failures.append(_failure("duplicate-path", f"registered audit path {path}"))
            continue
        if not isinstance(blob, str) or re.fullmatch(r"[0-9a-f]{40}", blob) is None:
            failures.append(
                _failure("audit-registry-entry", f"{path}: invalid Git blob pin")
            )
            continue
        registered[path] = blob

    candidates = tracked | set(registered)
    iteration_paths = sorted(
        path
        for path in candidates
        if path.startswith("wiki/audit/")
        and path.lower().endswith(".md")
        and AUDIT_ITERATION_KIND_RE.search(PurePosixPath(path).name)
        and path not in FIXED_AUDIT_ITERATION_EXCEPTIONS
    )
    receipt_paths = sorted(
        path for path in candidates if CONSOLIDATION_RECEIPT_PATH_RE.fullmatch(path)
    )
    state_paths = (*iteration_paths, *receipt_paths)
    raw_cache: dict[str, bytes] = {}

    def state_raw(path: str) -> bytes | None:
        if path in raw_cache:
            return raw_cache[path]
        if path not in tracked:
            failures.append(_failure("audit-epoch-state-invalid", f"{path}: not stage-0"))
            return None
        if path not in registered:
            failures.append(_failure("audit-artifact-unregistered", path))
        try:
            raw = read_bytes(path)
        except Exception as exc:
            failures.append(_failure("audit-artifact-missing", f"{path}: {exc}"))
            return None
        if not isinstance(raw, bytes):
            failures.append(_failure("audit-artifact-missing", f"{path}: bytes required"))
            return None
        raw_cache[path] = raw
        pin = registered.get(path)
        if pin is not None:
            actual_blob = _git_blob_sha1(raw)
            if actual_blob != pin:
                failures.append(
                    _failure(
                        "audit-registry-blob-mismatch",
                        f"{path}: raw {actual_blob} != pinned {pin}",
                    )
                )
        return raw

    for path in state_paths:
        state_raw(path)

    receipts: dict[tuple[str, int], dict[str, object]] = {}
    for path in receipt_paths:
        match = CONSOLIDATION_RECEIPT_PATH_RE.fullmatch(path)
        assert match is not None
        key = (match.group("campaign"), int(match.group("epoch")))
        raw = raw_cache.get(path)
        if raw is None:
            continue
        try:
            receipt = loads_json_strict(raw, path)
        except ContextSurfaceError as exc:
            failures.append(_failure("consolidation-epoch-invalid", str(exc)))
            continue
        if not isinstance(receipt, dict) or set(receipt) != CONSOLIDATION_RECEIPT_KEYS:
            failures.append(
                _failure("consolidation-epoch-invalid", f"{path}: exact receipt schema")
            )
            continue
        campaign, epoch = key
        if (
            receipt.get("schema") != CONSOLIDATION_RECEIPT_SCHEMA
            or receipt.get("campaign") != campaign
            or receipt.get("epoch") != epoch
        ):
            failures.append(
                _failure("consolidation-epoch-invalid", f"{path}: path identity mismatch")
            )
            continue
        effective_spec = receipt.get("effective_spec")
        try:
            effective_spec = _canonical_path(
                effective_spec, f"{path}.effective_spec"
            )
        except ContextSurfaceError as exc:
            failures.append(_failure("consolidation-epoch-invalid", str(exc)))
            continue
        version = receipt.get("effective_spec_version")
        sha256 = receipt.get("effective_spec_sha256")
        if (
            not effective_spec.startswith("wiki/survey/current/")
            or isinstance(version, bool)
            or not isinstance(version, int)
            or version <= 0
            or not isinstance(sha256, str)
            or SHA256_RE.fullmatch(sha256) is None
        ):
            failures.append(
                _failure("consolidation-epoch-invalid", f"{path}: spec binding fields")
            )
            continue
        if resolve_effective_spec(effective_spec) not in tracked:
            failures.append(
                _failure(
                    "consolidation-epoch-invalid",
                    f"{path}: effective spec is not stage-0",
                )
            )
            continue
        try:
            spec_raw = read_bytes(resolve_effective_spec(effective_spec))
        except Exception as exc:
            failures.append(
                _failure("consolidation-epoch-invalid", f"{effective_spec}: {exc}")
            )
            continue
        if not isinstance(spec_raw, bytes):
            failures.append(
                _failure("consolidation-epoch-invalid", f"{effective_spec}: bytes required")
            )
            continue
        if (
            _front_matter_protocol_version(spec_raw, effective_spec) != version
            or hashlib.sha256(spec_raw).hexdigest() != sha256
        ):
            failures.append(
                _failure("consolidation-epoch-invalid", f"{path}: forged spec binding")
            )
        receipts[key] = {
            "path": path,
            "effective_spec": effective_spec,
            "effective_spec_version": version,
            "effective_spec_sha256": sha256,
        }

    iterations: dict[tuple[str, int], list[tuple[int, str, dict[str, object]]]] = {}
    for path in iteration_paths:
        match = AUDIT_ITERATION_PATH_RE.fullmatch(path)
        if match is None:
            failures.append(_failure("audit-epoch-state-invalid", f"{path}: path shape"))
            continue
        campaign = match.group("campaign")
        epoch = int(match.group("epoch"))
        ordinal = int(match.group("ordinal"))
        kind = match.group("kind").lower()
        if ordinal >= 4:
            failures.append(_failure("unconsolidated-amendment-forbidden", path))
        raw = raw_cache.get(path)
        if raw is None:
            continue
        try:
            metadata = _parse_audit_iteration_front_matter(raw, path)
        except ContextSurfaceError as exc:
            failures.append(str(exc))
            continue
        if (
            metadata.get("campaign") != campaign
            or metadata.get("epoch") != epoch
            or metadata.get("ordinal") != ordinal
            or metadata.get("kind") != kind
        ):
            failures.append(
                _failure("audit-iteration-metadata-invalid", f"{path}: path identity")
            )
        iterations.setdefault((campaign, epoch), []).append(
            (ordinal, path, metadata)
        )

    epoch_keys = set(receipts) | set(iterations)
    campaigns = sorted({campaign for campaign, _epoch in epoch_keys})
    for campaign in campaigns:
        epochs = sorted(epoch for owner, epoch in epoch_keys if owner == campaign)
        if epochs != list(range(1, max(epochs) + 1)):
            failures.append(
                _failure(
                    "audit-epoch-state-invalid",
                    f"{campaign}: epochs must be continuous from 1, found {epochs}",
                )
            )
        for epoch in epochs:
            key = (campaign, epoch)
            receipt = receipts.get(key)
            if receipt is None:
                failures.append(
                    _failure(
                        "consolidation-epoch-invalid",
                        f"{campaign}/epoch-{epoch}: registered receipt required",
                    )
                )
            rows = iterations.get(key, [])
            ordinals = [ordinal for ordinal, _path, _metadata in rows]
            if len(ordinals) != len(set(ordinals)):
                failures.append(
                    _failure(
                        "audit-epoch-state-invalid",
                        f"{campaign}/epoch-{epoch}: duplicate ordinals {ordinals}",
                    )
                )
            if ordinals:
                unique = sorted(set(ordinals))
                if unique[-1] > 3 or unique != list(range(1, unique[-1] + 1)):
                    failures.append(
                        _failure(
                            "audit-epoch-state-invalid",
                            f"{campaign}/epoch-{epoch}: ordinals must be continuous 1..3",
                        )
                    )
            if receipt is not None:
                for _ordinal, path, metadata in rows:
                    for field in (
                        "effective_spec",
                        "effective_spec_version",
                        "effective_spec_sha256",
                    ):
                        if metadata.get(field) != receipt.get(field):
                            failures.append(
                                _failure(
                                    "audit-iteration-metadata-invalid",
                                    f"{path}: {field} differs from epoch receipt",
                                )
                            )

        highest = epochs[-1]
        receipt = receipts.get((campaign, highest))
        if receipt is None:
            continue
        if receipt.get("effective_spec") != EFFECTIVE_PROTOCOL_PATH:
            failures.append(
                _failure(
                    "consolidation-epoch-invalid",
                    f"{campaign}/epoch-{highest}: highest receipt must bind "
                    f"{EFFECTIVE_PROTOCOL_PATH}",
                )
            )
            continue
        resolved_spec = resolve_effective_spec(EFFECTIVE_PROTOCOL_PATH)
        spec_raw = read_bytes(resolved_spec)
        if (
            not isinstance(spec_raw, bytes)
            or hashlib.sha256(spec_raw).hexdigest()
            != receipt.get("effective_spec_sha256")
        ):
            failures.append(
                _failure(
                    "consolidation-epoch-invalid",
                    f"{campaign}/epoch-{highest}: archived protocol binding",
                )
            )

    return failures


def _validate_numbered_audit_iteration(
    path: str,
    ordinal: int,
    tracked: set[str],
    read_repo_path,
    failures: list[str],
) -> None:
    """Bind a numbered audit iteration to one immutable consolidation epoch."""

    if ordinal >= 4:
        failures.append(_failure("unconsolidated-amendment-forbidden", path))
        return
    parts = PurePosixPath(path).parts
    if len(parts) < 6 or parts[:2] != ("wiki", "audit"):
        failures.append(_failure("consolidation-epoch-invalid", f"{path}: path shape"))
        return
    campaign = parts[2]
    epoch_match = EPOCH_DIRECTORY_RE.fullmatch(parts[3])
    if epoch_match is None:
        failures.append(
            _failure("consolidation-epoch-invalid", f"{path}: missing epoch-<N>")
        )
        return
    epoch = int(epoch_match.group(1))
    receipt_path = f"wiki/audit/{campaign}/epoch-{epoch}/consolidation-receipt.json"
    if receipt_path not in tracked:
        failures.append(
            _failure("consolidation-epoch-invalid", f"{path}: missing {receipt_path}")
        )
        return
    receipt_raw = read_repo_path(receipt_path, "consolidation-receipt-missing")
    if receipt_raw is None:
        failures.append(_failure("consolidation-epoch-invalid", receipt_path))
        return
    try:
        receipt = loads_json_strict(receipt_raw, receipt_path)
    except ContextSurfaceError as exc:
        failures.append(_failure("consolidation-epoch-invalid", str(exc)))
        return
    if not isinstance(receipt, dict) or set(receipt) != CONSOLIDATION_RECEIPT_KEYS:
        failures.append(
            _failure("consolidation-epoch-invalid", f"{receipt_path}: exact schema fields")
        )
        return
    if (
        receipt.get("schema") != CONSOLIDATION_RECEIPT_SCHEMA
        or receipt.get("campaign") != campaign
        or receipt.get("epoch") != epoch
    ):
        failures.append(
            _failure("consolidation-epoch-invalid", f"{receipt_path}: campaign/epoch")
        )
        return
    try:
        effective_spec = _canonical_path(
            receipt.get("effective_spec"), f"{receipt_path}.effective_spec"
        )
    except ContextSurfaceError as exc:
        failures.append(_failure("consolidation-epoch-invalid", str(exc)))
        return
    resolved_spec = resolve_effective_spec(effective_spec)
    if not effective_spec.startswith("wiki/survey/current/") or resolved_spec not in tracked:
        failures.append(
            _failure(
                "consolidation-epoch-invalid",
                f"{receipt_path}: effective spec must resolve to a tracked carrier",
            )
        )
        return
    spec_raw = read_repo_path(resolved_spec, "consolidation-effective-spec-missing")
    if spec_raw is None:
        failures.append(_failure("consolidation-epoch-invalid", effective_spec))
        return
    version = receipt.get("effective_spec_version")
    if (
        isinstance(version, bool)
        or not isinstance(version, int)
        or version <= 0
        or _front_matter_protocol_version(spec_raw, effective_spec) != version
    ):
        failures.append(
            _failure("consolidation-epoch-invalid", f"{receipt_path}: spec version")
        )
    expected_hash = receipt.get("effective_spec_sha256")
    if (
        not isinstance(expected_hash, str)
        or SHA256_RE.fullmatch(expected_hash) is None
        or hashlib.sha256(spec_raw).hexdigest() != expected_hash
    ):
        failures.append(
            _failure("consolidation-epoch-invalid", f"{receipt_path}: spec sha256")
        )


def evaluate_manifest(repo, manifest, tracked_paths):
    """Evaluate a parsed manifest against an explicit tracked-path inventory."""

    failures: list[str] = []
    try:
        reader = TrustedRepoReader(repo)
    except ContextSurfaceError as exc:
        return [str(exc)]
    _, active, budgets, legacy_entries, active_review = _validate_manifest_shape(manifest, failures)

    try:
        legacy = _legacy_map(legacy_entries)
    except ContextSurfaceError as exc:
        failures.append(str(exc))
        legacy = {}
        legacy_entries = []

    canonical_tracked: list[str] = []
    tracked_seen: set[str] = set()
    if not isinstance(tracked_paths, (list, tuple)):
        failures.append(
            _failure("manifest-schema-invalid", "tracked_paths must be an explicit list")
        )
        tracked_paths = []
    for index, path in enumerate(tracked_paths):
        try:
            canonical = _canonical_path(path, f"tracked_paths[{index}]")
        except ContextSurfaceError as exc:
            failures.append(str(exc))
            continue
        if canonical in tracked_seen:
            failures.append(_failure("duplicate-path", f"tracked path {canonical}"))
            continue
        tracked_seen.add(canonical)
        canonical_tracked.append(canonical)

    raw_cache: dict[str, bytes] = {}

    def read_repo_path(path: str, missing_code: str):
        if path in raw_cache:
            return raw_cache[path]
        try:
            raw = reader.read_bytes(path)
        except ContextSurfaceError as exc:
            if str(exc).startswith("repo-path-missing:"):
                failures.append(_failure(missing_code, path))
            else:
                failures.append(str(exc))
            return None
        raw_cache[path] = raw
        return raw

    for path in legacy:
        if path not in tracked_seen:
            failures.append(_failure("legacy-path-untracked", path))
        read_repo_path(path, "legacy-path-missing")

    canonical_review: str | None = None
    if active_review is not None:
        try:
            canonical_review = _canonical_path(active_review, "active_review_transaction")
            if not canonical_review.startswith(
                "wiki/audit/"
            ) or canonical_review.endswith("/INDEX.md"):
                failures.append(
                    _failure(
                        "manifest-schema-invalid",
                        "active_review_transaction must be one exact audit-round artifact",
                    )
                )
            if canonical_review not in tracked_seen:
                failures.append(
                    _failure("active-review-transaction-untracked", canonical_review)
                )
            read_repo_path(canonical_review, "active-review-transaction-missing")
        except ContextSurfaceError as exc:
            failures.append(str(exc))

    if len(active) > 30:
        failures.append(
            _failure("active-entry-budget-exceeded", f"{len(active)} active entries exceeds 30")
        )

    active_seen: set[str] = set()
    for index, entry in enumerate(active):
        if not isinstance(entry, dict):
            failures.append(
                _failure("manifest-entry-invalid", f"active_entries[{index}] must be an object")
            )
            continue
        raw_path = entry.get("path")
        is_self = raw_path == MANIFEST_RELATIVE_PATH
        expected_keys = SELF_ENTRY_KEYS if is_self else ENTRY_KEYS
        if set(entry) != expected_keys:
            failures.append(
                _failure(
                    "manifest-entry-invalid",
                    f"active_entries[{index}] keys must be exactly {sorted(expected_keys)}",
                )
            )
        try:
            path = _canonical_path(raw_path, f"active_entries[{index}].path")
        except ContextSurfaceError as exc:
            failures.append(str(exc))
            continue
        if path in active_seen:
            failures.append(_failure("duplicate-path", f"active path {path}"))
            continue
        active_seen.add(path)
        if path in legacy:
            failures.append(_failure("active-legacy-overlap", path))
        # The only pre-git-add bootstrap exception: the exact manifest self
        # metadata may be untracked after the builder has written it.  The
        # trusted read below still requires a regular non-symlink at that path.
        bootstrap_self = is_self and path not in tracked_seen
        if path not in tracked_seen and not bootstrap_self:
            failures.append(_failure("active-path-untracked", path))
        try:
            actual_class = classify_path(path, legacy_entries)
        except ContextSurfaceError as exc:
            failures.append(str(exc))
            actual_class = "UNCLASSIFIED"
        declared_class = entry.get("class")
        if not isinstance(declared_class, str):
            failures.append(_failure("manifest-entry-invalid", f"{path}: class must be a string"))
        if declared_class != actual_class:
            failures.append(
                _failure(
                    "active-class-mismatch",
                    f"{path}: declared {declared_class!r}, classified {actual_class!r}",
                )
            )
        if actual_class in COLD_ACTIVE_CLASSES or (
            isinstance(declared_class, str) and declared_class in COLD_ACTIVE_CLASSES
        ):
            failures.append(
                _failure("cold-path-on-active-surface", f"{path}: {actual_class}")
            )
        if not isinstance(entry.get("load_policy"), str) or entry.get("load_policy") not in {
            "default",
            "targeted",
        }:
            failures.append(
                _failure("manifest-entry-invalid", f"{path}: invalid load_policy")
            )
        if not isinstance(entry.get("purpose"), str) or not entry.get("purpose", "").strip():
            failures.append(
                _failure("manifest-entry-invalid", f"{path}: purpose must be non-empty")
            )
        sha256 = entry.get("sha256")
        if not is_self and (not isinstance(sha256, str) or SHA256_RE.fullmatch(sha256) is None):
            failures.append(_failure("manifest-entry-invalid", f"{path}: invalid sha256"))
        raw = read_repo_path(path, "active-path-missing")
        if raw is None:
            continue
        if not is_self and isinstance(sha256, str) and SHA256_RE.fullmatch(sha256):
            actual_hash = hashlib.sha256(raw).hexdigest()
            if actual_hash != sha256:
                failures.append(
                    _failure("active-hash-mismatch", f"{path}: {actual_hash} != {sha256}")
                )

    budget_seen: set[str] = set()
    for raw_path, limit in budgets.items():
        try:
            path = _canonical_path(raw_path, "budgets_bytes key")
        except ContextSurfaceError as exc:
            failures.append(str(exc))
            continue
        if path in budget_seen:
            failures.append(_failure("duplicate-path", f"budget path {path}"))
            continue
        budget_seen.add(path)
        if path not in tracked_seen:
            failures.append(_failure("budget-path-untracked", path))
        if isinstance(limit, bool) or not isinstance(limit, int) or limit < 0:
            failures.append(
                _failure(
                    "manifest-schema-invalid",
                    f"budget for {path} must be a non-negative integer",
                )
            )
            continue
        raw = read_repo_path(path, "budget-path-missing")
        if raw is not None and len(raw) > limit:
            failures.append(
                _failure("file-budget-exceeded", f"{path}: {len(raw)} > {limit} raw bytes")
            )

    for path in canonical_tracked:
        path_class = (
            classify_path(path, legacy_entries)
            if legacy_entries
            else classify_path(path, [])
        )
        basename = PurePosixPath(path).name
        is_legacy = path in legacy
        if (
            (path.startswith("wiki/") and path.lower().endswith(".md"))
            or path in {"AGENTS.md", "CLAUDE.md", "CONTRIBUTING.md"}
        ) and path_class == "UNCLASSIFIED":
            failures.append(_failure("unclassified-persistent-document", path))
        if (
            path.startswith("wiki/")
            and path.lower().endswith(".md")
            and AUDIT_NAME_RE.search(basename)
            and not path.startswith(("wiki/audit/", "wiki/archive/"))
            and not is_legacy
        ):
            failures.append(_failure("new-audit-artifact-outside-audit-root", path))
        numbered_iteration = (
            NUMBERED_ITERATION_RE.search(basename)
            if path.startswith("wiki/") and path.lower().endswith(".md")
            else None
        )
        is_new_audit_iteration = (
            path.startswith("wiki/audit/")
            and path.lower().endswith(".md")
            and AUDIT_ITERATION_KIND_RE.search(basename) is not None
            and path not in FIXED_AUDIT_ITERATION_EXCEPTIONS
        )
        if is_new_audit_iteration and AUDIT_ITERATION_PATH_RE.fullmatch(path) is None:
            failures.append(_failure("audit-epoch-state-invalid", f"{path}: path shape"))
        if numbered_iteration and not path.startswith("wiki/archive/") and not is_legacy:
            ordinal = int(numbered_iteration.group(1))
            if path.startswith("wiki/audit/"):
                _validate_numbered_audit_iteration(
                    path,
                    ordinal,
                    tracked_seen,
                    read_repo_path,
                    failures,
                )
            elif ordinal >= 4:
                failures.append(_failure("unconsolidated-amendment-forbidden", path))
        if path_class != "HOT" or not path.lower().endswith(".md"):
            continue
        raw = read_repo_path(path, "persistent-path-missing")
        if raw is None:
            continue
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            failures.append(_failure("active-file-invalid-utf8", f"{path}: {exc}"))
            continue
        link_text = _mask_markdown_code(text)
        for raw_target in _link_targets(link_text):
            try:
                target = _normalize_link_target(path, raw_target)
            except ContextSurfaceError as exc:
                failures.append(str(exc))
                continue
            if (
                target is not None
                and _is_direct_audit_round_link(target)
                and target != canonical_review
            ):
                failures.append(_failure("direct-audit-round-link", f"{path} -> {target}"))

    guide_paths = {"AGENTS.md", "CLAUDE.md"}
    if guide_paths.issubset(tracked_seen):
        try:
            agents_raw = read_repo_path("AGENTS.md", "agent-guide-missing")
            claude_raw = read_repo_path("CLAUDE.md", "agent-guide-missing")
            if agents_raw is None or claude_raw is None:
                return failures
            agents = agents_raw.decode("utf-8")
            claude = claude_raw.decode("utf-8")
            if normalize_agent_guide(agents) != normalize_agent_guide(claude):
                failures.append(
                    _failure(
                        "agent-guides-not-mirrored",
                        "shared guidance differs beyond 3 client lines",
                    )
                )
        except (UnicodeDecodeError, ContextSurfaceError, TypeError) as exc:
            failures.append(_failure("agent-guides-not-mirrored", str(exc)))

    policy_path = "wiki/AI-Collaboration.md"
    if policy_path in tracked_seen:
        policy_raw = read_repo_path(policy_path, "collaboration-policy-missing")
        if policy_raw is not None:
            try:
                policy_text = policy_raw.decode("utf-8")
            except UnicodeDecodeError as exc:
                failures.append(_policy_invalid(f"invalid UTF-8: {exc}"))
            else:
                failures.extend(validate_collaboration_policy(policy_text))

    return failures


def _resolved_gitdir(
    dot_git: Path, platform: str = os.name
) -> Path | PurePosixPath:
    """Resolve a native-Windows linked-worktree pointer on Windows or WSL."""

    try:
        pointer = dot_git.read_text(encoding="utf-8").strip()
    except OSError as exc:
        raise ContextSurfaceError(
            _failure("git-worktree-pointer-invalid", str(exc))
        ) from exc
    prefix = "gitdir: "
    if not pointer.startswith(prefix) or "\n" in pointer or "\r" in pointer:
        raise ContextSurfaceError(
            _failure("git-worktree-pointer-invalid", str(dot_git))
        )
    raw = pointer[len(prefix) :]
    windows_absolute = re.fullmatch(r"([A-Za-z]):[\\/](.*)", raw)
    if windows_absolute:
        if platform == "posix":
            drive, remainder = windows_absolute.groups()
            return PurePosixPath(
                f"/mnt/{drive.lower()}/{remainder.replace('\\', '/')}"
            )
        return Path(raw)
    candidate = Path(raw)
    return candidate if candidate.is_absolute() else dot_git.parent / candidate


def git_command_prefix(repo: Path, platform: str = os.name) -> list[str]:
    """Return a Git command prefix that works for native linked worktrees in WSL."""

    repo = Path(repo)
    command = ["git"]
    dot_git = repo / ".git"
    if dot_git.is_file():
        command.extend(
            [
                f"--git-dir={_resolved_gitdir(dot_git, platform)}",
                f"--work-tree={repo}",
            ]
        )
    return command


def _git_tracked_paths(repo: Path) -> list[str]:
    try:
        completed = subprocess.run(
            [*git_command_prefix(repo), "ls-files", "-z"],
            cwd=repo,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError as exc:
        raise ContextSurfaceError(_failure("git-ls-files-failed", str(exc))) from exc
    if completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", errors="replace").strip()
        raise ContextSurfaceError(_failure("git-ls-files-failed", detail))
    try:
        return [part.decode("utf-8") for part in completed.stdout.split(b"\0") if part]
    except UnicodeDecodeError as exc:
        raise ContextSurfaceError(
            _failure("git-ls-files-failed", f"non-UTF-8 path: {exc}")
        ) from exc


def main() -> int:
    repo = Path(__file__).resolve().parents[2]
    try:
        tracked = _git_tracked_paths(repo)
        document = loads_json_strict(
            TrustedRepoReader(repo).read_bytes(MANIFEST_RELATIVE_PATH),
            MANIFEST_RELATIVE_PATH,
        )
        failures = evaluate_manifest(repo, document, tracked)
    except ContextSurfaceError as exc:
        failures = [str(exc)]
    for failure in failures:
        print(failure)
    print(f"AI context surface: {'FAIL' if failures else 'PASS'} ({len(failures)} failures)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
