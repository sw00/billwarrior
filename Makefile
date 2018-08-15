init:
	pip install -r requirements.txt

test:
	python test_billable.py

.PHONY:
	init test
