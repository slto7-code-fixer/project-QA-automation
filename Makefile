VENV=.venv
PY=python3

.PHONY: venv install install-dev lint test test-playwright report clean

venv:
	$(PY) -m venv $(VENV)

install: venv
	. $(VENV)/bin/activate && pip install -r requirements.txt

install-dev: venv
	. $(VENV)/bin/activate && pip install -r requirements-dev.txt

test:
	pytest -q

test-playwright:
	python -m playwright install chromium && pytest --alluredir=allure-results -q

report:
	pytest --html=report.html --alluredir=allure-results -q

clean:
	rm -rf $(VENV) .pytest_cache __pycache__ report.html
