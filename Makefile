run:
	py test.py

lint:
	black -l 79 .
	flake8 .
