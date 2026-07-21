.PHONY: check test

check:
	python3 -m unittest discover -s tests -v
	python3 bin/validate_reference.py
	@bash -n start.sh

test:
	python3 -m unittest discover -s tests -v
