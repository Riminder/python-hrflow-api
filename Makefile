# Define variables
ARGS := 

clean:
	rm -rf build dist *.egg-info

clean_cache:
	find . -type d \( -name '__pycache__' -o -name '.pytest_cache' \) -exec rm -rf {} +
	rm -rf tests/assets

build:
	poetry build

git-tag:
	./tag.sh $(ARGS)

deploy-test:
	poetry publish -r test-pypi --build

deploy:
	poetry publish --build

flake8:
	poetry run flake8 --config=./.flake8

style:
	poetry run isort . && poetry run black --config=./pyproject.toml .

check:
	bash ./check.sh