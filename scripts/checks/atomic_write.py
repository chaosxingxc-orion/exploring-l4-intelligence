#!/usr/bin/env python3
"""Durable atomic byte publication (extracted verbatim from the retired
sf_query_compiler on 2026-08-03 so surviving checks keep one shared
implementation)."""

from __future__ import annotations

import os
import stat
import tempfile
from pathlib import Path


class AtomicPublishRollbackError(OSError):
    """A publish failed and at least one required rollback action also failed."""

    def __init__(
        self,
        publish_error: BaseException,
        rollback_failures: list[tuple[str, BaseException]],
        recovery_backup: Path | None,
    ):
        self.publish_error = publish_error
        self.rollback_failures = tuple(rollback_failures)
        self.recovery_backup = recovery_backup
        rollback_text = "; ".join(
            f"{operation}: {error}" for operation, error in rollback_failures
        )
        recovery_text = (
            f"; recovery backup retained at {recovery_backup}"
            if recovery_backup is not None
            else ""
        )

def _cleanup_created_directories(created: list[Path]) -> None:
    """Remove only empty directories created by this invocation."""
    for directory in reversed(created):
        try:
            directory.rmdir()
        except OSError:
            # A concurrent writer may have populated it.  Never recurse and
            # never remove anything that is no longer empty.
            pass


def _create_parent_chain(parent: Path) -> list[Path]:
    """Create missing parents and return exactly the directories we created."""
    missing: list[Path] = []
    cursor = parent
    while not cursor.exists():
        missing.append(cursor)
        cursor = cursor.parent

    created: list[Path] = []
    try:
        for directory in reversed(missing):
            try:
                directory.mkdir()
            except FileExistsError:
                if not directory.is_dir():
                    raise
            else:
                created.append(directory)
    except BaseException:
        _cleanup_created_directories(created)
        raise
    return created


def fsync_parent_directory(parent: Path) -> None:
    """Durably publish a rename on POSIX; Windows has no directory fsync API."""
    if os.name != "posix":
        return
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
    fd = os.open(str(parent), flags)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def _stage_existing_target_backup(destination: Path) -> Path:
    """Create and durably stage a same-directory raw-byte/mode backup."""
    original_bytes = destination.read_bytes()
    original_mode = stat.S_IMODE(destination.stat().st_mode)
    fd, raw_backup = tempfile.mkstemp(
        prefix=f".{destination.name}.", suffix=".bak", dir=destination.parent
    )
    backup_path = Path(raw_backup)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(original_bytes)
            handle.flush()
            os.fsync(handle.fileno())
        backup_path.chmod(original_mode)
        # Persist the mode change as well as the raw bytes before publication.
        with backup_path.open("r+b") as handle:
            os.fsync(handle.fileno())
        if backup_path.read_bytes() != original_bytes:
            raise OSError(f"backup verification failed: {backup_path}")
        if stat.S_IMODE(backup_path.stat().st_mode) != original_mode:
            raise OSError(f"backup mode verification failed: {backup_path}")
        return backup_path
    except BaseException:
        try:
            os.close(fd)
        except OSError:
            pass
        backup_path.unlink(missing_ok=True)
        raise


def atomic_write_bytes(destination: Path, payload: bytes) -> None:
    """Durably publish bytes or restore the exact pre-call target state."""
    destination = Path(destination)
    created = _create_parent_chain(destination.parent)
    temp_path: Path | None = None
    backup_path: Path | None = None
    destination_existed = False
    try:
        fd, raw_temp = tempfile.mkstemp(
            prefix=f".{destination.name}.", suffix=".tmp", dir=destination.parent
        )
        temp_path = Path(raw_temp)
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        if temp_path.read_bytes() != payload:
            raise OSError(f"staged output verification failed: {temp_path}")

        destination_existed = destination.exists()
        if destination_existed:
            if not destination.is_file():
                raise OSError(f"destination is not a regular file: {destination}")
            backup_path = _stage_existing_target_backup(destination)
            # The backup's file data/mode and directory entry must be durable
            # before the old target is exposed to replacement.
            fsync_parent_directory(destination.parent)

        os.replace(temp_path, destination)
        temp_path = None
    except BaseException:
        try:
            if temp_path is not None:
                temp_path.unlink(missing_ok=True)
            if backup_path is not None:
                backup_path.unlink(missing_ok=True)
            _cleanup_created_directories(created)
        finally:
            raise

    try:
        fsync_parent_directory(destination.parent)
    except BaseException as publish_error:
        rollback_failures: list[tuple[str, BaseException]] = []
        rollback_changed_parent = False
        if destination_existed:
            try:
                os.replace(backup_path, destination)
                backup_path = None
                rollback_changed_parent = True
            except BaseException as rollback_error:
                rollback_failures.append(("restore-existing-target", rollback_error))
        else:
            try:
                destination.unlink()
                rollback_changed_parent = True
            except BaseException as rollback_error:
                rollback_failures.append(("remove-fresh-target", rollback_error))

        if rollback_changed_parent:
            try:
                fsync_parent_directory(destination.parent)
            except BaseException as rollback_error:
                rollback_failures.append(("fsync-rollback-parent", rollback_error))

        # A fresh target owns its newly-created parent chain.  Successful
        # unlinking leaves those directories empty; a failed unlink leaves
        # them intact and rmdir safely declines to remove them.
        if not destination_existed:
            _cleanup_created_directories(created)

        if rollback_failures:
            raise AtomicPublishRollbackError(
                publish_error,
                rollback_failures,
                backup_path,
            ) from publish_error
        raise

    if backup_path is not None:
        backup_path.unlink()


# ---------------------------------------------------------------------------
# Static validation
# ---------------------------------------------------------------------------

CJK_RANGES = (
    (0x3400, 0x4DBF), (0x4E00, 0x9FFF), (0xF900, 0xFAFF),
    (0x3000, 0x303F),  # CJK punctuation (includes full-width parens etc.)
    (0xFF00, 0xFFEF),  # full-width forms
)


