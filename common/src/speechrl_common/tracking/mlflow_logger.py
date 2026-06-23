"""Local-MLflow helper. No server needed — runs are written to a local file store.

Usage:
    from speechrl_common.tracking.mlflow_logger import mlflow_run
    with mlflow_run("training-free-rl", "baseline-v1", params={"lr": 1e-6}) as run:
        ... mlflow.log_metric("reward", r, step=i) ...

Inspect with:  mlflow ui --backend-store-uri <SPEECHRL_MLFLOW_DIR>
"""
from __future__ import annotations

import os
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator


def tracking_uri() -> str:
    """Local file-store URI. Override with SPEECHRL_MLFLOW_DIR."""
    env = os.environ.get("SPEECHRL_MLFLOW_DIR")
    root = Path(env) if env else Path.home() / "speechrl-data" / "mlruns"
    root.mkdir(parents=True, exist_ok=True)
    # mlflow wants a file: URI on local stores
    return root.resolve().as_uri()


@contextmanager
def mlflow_run(
    experiment: str,
    run_name: str,
    *,
    params: dict[str, Any] | None = None,
    tags: dict[str, str] | None = None,
) -> Iterator[Any]:
    """Context manager that opens an MLflow run against the local store."""
    import mlflow  # lazy

    # mlflow >= 3 puts the file store in "maintenance mode" and raises unless this opt-out is set.
    # The local file store is this project's intentional, server-less tracking design (see module
    # docstring and scripts/mlflow-ui.sh), so opt back in rather than require a DB backend.
    os.environ.setdefault("MLFLOW_ALLOW_FILE_STORE", "true")
    mlflow.set_tracking_uri(tracking_uri())
    mlflow.set_experiment(experiment)
    with mlflow.start_run(run_name=run_name, tags=tags) as run:
        if params:
            mlflow.log_params(params)
        yield run
