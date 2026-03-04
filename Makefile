.PHONY: setup run test install-deps clean

setup:
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt

run:
	bash scripts/run_resume_editor.sh

test:
	bash scripts/test_resume_editor.sh

install-deps:
	. venv/bin/activate && pip install -r requirements.txt

clean:
	rm -rf venv __pycache__
