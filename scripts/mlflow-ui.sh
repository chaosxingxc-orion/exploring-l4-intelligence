#!/usr/bin/env bash
# Launch the local MLflow UI against the file store (no server/account needed).
set -euo pipefail
DIR="${SPEECHRL_MLFLOW_DIR:-$HOME/speechrl-data/mlruns}"
mkdir -p "$DIR"
echo "MLflow UI -> http://127.0.0.1:5000   (store: $DIR)"
exec mlflow ui --backend-store-uri "$DIR" --host 127.0.0.1 --port 5000
