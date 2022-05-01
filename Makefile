ROOT := $(shell pwd)
SYSTEM := $(shell uname -s)

VENV := venv
ACTIVATE := . $(VENV)/bin/activate;


.PHONY: all
all: clean test lint

.PHONY: setup-venv
setup-venv:
	python3 -m venv venv
	$(ACTIVATE) pip3 install --upgrade pip
	$(ACTIVATE) pip3 install -r requirements.txt
	$(ACTIVATE) pip3 install -r requirements-dev.txt

.PHONY: remove-venv
remove-venv:
	rm -rf venv

.PHONY: install-deps
install-deps:
ifeq ($(SYSTEM), Darwin)
	$(ACTIVATE) pip3 install --upgrade pip
	$(ACTIVATE) pip3 install -r requirements.txt
	$(ACTIVATE) pip3 install -r requirements-dev.txt
else
	pip3 install --upgrade pip
	pip3 install -r requirements.txt
	pip3 install -r requirements-dev.txt
endif

.PHONY: clean
clean:
	rm -rf .coverage deployment-package.zip htmlcov package
	find . -name __pycache__ -prune -exec rm -rf {} \;

.PHONY: test
test:
ifeq ($(SYSTEM), Darwin)
	$(ACTIVATE) pytest --cov=app tests
else
	pytest --cov=app tests
endif

.PHONY: coverage
coverage: .coverage
ifeq ($(SYSTEM), Darwin)
	$(ACTIVATE) coverage report -m
	@echo
	$(ACTIVATE) coverage html
	@echo
	open htmlcov/index.html
else
	coverage report -m
	@echo
	coverage html
endif

.PHONY: lint
lint:
ifeq ($(SYSTEM), Darwin)
	$(ACTIVATE) pylint --rcfile=.pylintrc-relaxed app tests
else
	pylint --rcfile=.pylintrc-relaxed app tests
endif

.PHONY: zip
zip:
	zip --recurse-paths deployment-package.zip app
	pip3 install --target ./package -r requirements.txt
# zip error 12 is "nothing to do" - ignore this, which happens when there are no dependencies
	cd package && zip --grow --recurse-paths ../deployment-package.zip . || [ $$? -eq 12 ]
	ls -lh deployment-package.zip

.PHONY: update-function-code
update-function-code:
ifeq ($(AWS_REGION),)
	echo "AWS_REGION must be set" && exit 1
endif
# filter output to avoid leaking lamba environment variables into workflow logs
	aws lambda update-function-code --function-name huggsy --zip-file fileb://deployment-package.zip |jq '{"Runtime": .Runtime, "Handler": .Handler, "CodeSize": .CodeSize, "CodeSha256": .CodeSha256}'

# DEBUG: print out a a variable via `make print-FOO`
print-%: ; @echo $* = $($*)
