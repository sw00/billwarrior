init:
	pipenv install --dev

test:
	pipenv run py.test tests

.PHONY:
	init test
