# Define variables
ARGS := 

install_req:
	pip install -U setuptools setuptools_scm wheel

clean:
	rm -rf build dist *.egg-info

build:
	python setup.py sdist bdist_wheel

git-tag:
	./tag.sh $(ARGS)

deploy-test:
	python -m pip install twine && twine upload --repository-url https://test.pypi.org/legacy/ dist/*

deploy:
	python -m pip install twine && twine upload dist/*