install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

# test
test:
	python -m pytest -vv --cov=main src/test_*.py
	# python -m pytest --nbval src/*.ipynb

# format
format:	
	black src/*.py
	black *.py
	black database/*.py
	nbqa black src/*.ipynb

# lint
lint:
	pylint --disable=R,C --disable=unnecessary-pass --ignore-patterns=test_.*?py src/*.py
	pylint --disable=R,C --disable=unnecessary-pass --ignore-patterns=test_.*?py *.py
	pylint --disable=R,C --disable=unnecessary-pass --ignore-patterns=test_.*?py database/*.py
	#nbqa ruff src/*.ipynb
	#ruff check src/*.py


# deploy

all: install lint format test 
