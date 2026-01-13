PYTHON ?= python3
PIP ?= $(PYTHON) -m pip

.PHONY: install run

install:
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) -m streamlit run decoder_app.py
