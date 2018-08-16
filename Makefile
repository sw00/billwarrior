init:
	pipenv install --dev

test:
	pipenv run py.test

.PHONY:
	init test
