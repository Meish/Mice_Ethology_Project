make install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

make lint: 
	pylint --disable=R,C,W1203,W0702,W0621 main.py || python pylint_exit.py $?

make format:
	black *.py
make test:
	python -m pytest -vv --cov=main test_main.py

	
