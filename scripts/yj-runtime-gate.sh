#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

python3 - <<'PY'
from pathlib import Path
import re

root = Path("projects/fc-exec-2515")
status = (root / "STATUS.yaml").read_text(encoding="utf-8")
current = (root / "CURRENT.yaml").read_text(encoding="utf-8")
manifest = (root / "PROJECT_MANIFEST.yaml").read_text(encoding="utf-8")

def scalar(text: str, key: str):
    m = re.search(rf"(?m)^\s*{re.escape(key)}:\s*([^#\n]+?)\s*$", text)
    return m.group(1).strip() if m else None

assert scalar(status, "project_id") == "FC-EXEC-2515-01"
assert scalar(status, "lifecycle") == "ACTIVE"
assert "status: SEALED" in status
assert "validation: PASS" in status
assert "blocker: null" in status
assert scalar(current, "project_id") == "FC-EXEC-2515-01"
assert scalar(current, "status") == "READY"
assert scalar(manifest, "project_id") == "FC-EXEC-2515-01"
assert scalar(manifest, "truth_root") == "projects/fc-exec-2515"
assert (root / "evidence/W3_SEGMENT_INDEX.csv").is_file()
assert (root / "scripts/w3_segmented_store.py").is_file()
print("FC_EXEC_2515_CONTROL_GATE=PASS")
PY
