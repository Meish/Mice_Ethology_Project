make install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

make lint: 
	pylint --disable=R,C,W1203,W0702 app.py

make format:
	black *.py

make test:
	python -m pytest -vv --cov=app test_app.py

make all: install lint format test
	
