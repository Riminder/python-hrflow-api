# Define variables
ARGS := 

clean:
	rm -rf build dist *.egg-info

build:
	python setup.py sdist bdist_wheel

git-tag:
	./tag.sh $(ARGS)

deploy-test:
	python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

deploy:
	python -m twine upload dist/*