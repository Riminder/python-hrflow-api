# Define variables
ARGS := 

clean:
	rm -rf build dist *.egg-info

build:
	poetry build

git-tag:
	./tag.sh $(ARGS)

deploy-test:
	poetry publish -r test-pypi --build

deploy:
	poetry publish --build