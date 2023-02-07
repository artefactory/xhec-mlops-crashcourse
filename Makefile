prepare-mlops-crashcourse: welcome build-all ready

launch-mlops-crashcourse: create-network run-all open-ui

clean-mlops-crashcourse: stop-all remove-all remove-network clean-mlflow goodbye

#################
# 	 DOCKER	    #
#################

create-network:
	@echo "Creating the course docker network..."
	-@docker network create --driver bridge mlops-crashcourse

remove-network:
	@echo "Removing the course docker network..."
	-@docker network rm mlops-crashcourse

build-all: build-lesson build-mlflow

build-lesson:
	@echo "Building lesson jupyter lab container..."
	@docker build -t mlops_notebooks ./lesson/

build-mlflow:
	@echo "Building lesson mlflow container..."
	@docker build -t mlops_mlflow ./mlflow_server/

remove-all:
	@echo "Removing all course images..."
	-@docker image rm mlops_notebooks
	-@docker image rm mlops_mlflow

run-all: run-lesson run-mlflow

run-lesson:
	./lesson/bin/run_lab.sh

run-mlflow:
	./mlflow_server/run_server.sh

stop-all:
	@echo "Stopping all course containers..."
	-@docker stop jupyter
	-@docker stop mlflow

clean-mlflow:
	@echo "Removing all mlflow data..."
	-@rm -rf ./mlflow_server/local/artifacts
	-@rm -rf ./mlflow_server/local/mlflow.db

#################
# 	 	CI	    #
#################

# help: run-linter				- lint code
.PHONY: run-linter
run-linter:
	@echo "Running linter and code formatting checks"
	@isort . --check --diff --profile black
	@black --check .
	@flake8 .

# help: install_precommit				- run pre-commit hooks
.PHONY: install-precommit
install-precommit:
	@pre-commit install -t pre-commit

# help: format-code				- run pre-commit hooks
.PHONY: format-code
format-code:
	@pre-commit run --all-files

#################
# 	   MISC	    #
#################

.PHONY: welcome
welcome:
	@echo
	@echo "Welcome to the Artefact MLOps crash course!"
	@echo "This util will prepare the course dependencies for you."
	@echo "If this fails, make sure Docker is installed and running."
	@echo "This might take a few minutes depending on your computer and connexion."
	@echo "Are you ready? [y/N] " && read ans && [ $${ans:-N} = y ]

.PHONY: ready
ready:
	@echo
	@echo "The docker images for the mlflow server and the jupyter lab have now been created."
	@echo "Thank you for your patience!"
	@echo "You can now run the command 'make launch-mlops-crashcourse' in the console to launch the course."
	@echo

.PHONY: goodbye
goodbye:
	@echo
	@echo "Thanks for participating in the Artefact MLOps crash course!"
	@echo

.PHONY: open-ui
open-ui:
	@open http://localhost:5001
	@open http://localhost:10000
