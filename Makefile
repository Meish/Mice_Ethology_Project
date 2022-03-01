make install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

make lint: 
	pylint --rcfile=.pylintrc --disable=R,C,W1203,W0702,W0621 main.py || pylint-exit $$? 

make format:
	black *.py

make test:
	python -m pytest -vv --cov=main test_main.py

	
