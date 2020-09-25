run:
	python app.py

lint:
	python -m black -l 79 .
	python -m flake8 .
