set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

if [[ ! -d "venv" ]]; then
	echo "Virtual environment not found. Run: make setup" >&2
	exit 1
fi

. venv/bin/activate 

cat >> logs/run_resume_editor.log << EOF

--------------------------------------------------------------------------------
APPLICATION RUN: $(date '+%Y-%m-%d %H:%M:%S')
--------------------------------------------------------------------------------

EOF

export PYTHONPATH="${PROJECT_ROOT}:${PYTHONPATH:-}"
python -m src.main 2>&1 | tee -a logs/run_resume_editor.log