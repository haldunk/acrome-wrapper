SHELL := /bin/bash

# Make management targets
.PHONY : help

help :
	@echo "Acrome SMD Wrapper Python Library"
	@echo "  help   - displays available make targets"
	@echo
	@echo " Virtual Environment Management"
	@echo "  venv-clear   - delete virtual environment"
	@echo "  venv-setup   - sets up a fresh virtual environment"
	@echo "  venv-install - installs/updates required packages"
	@echo "  venv-pack    - updates required packages listing"
	@echo
	@echo " Development Management"
	@echo "  clean  - delete all temporary files"
	@echo "  test   - runs unit tests"
	@echo
	@echo " Package Management"
	@echo "  clear   - delete compiled package"
	@echo "  build   - build compiled package"
	@echo "  install - install compiled package locally"


# Virtual environment management targets
.PHONY : venv-clear venv-setup venv-install venv-pack

venv-clear :
	@echo "Delete existing virtual environment"
	@rm -rf venv

venv-setup : venv-clear
	@echo "Setup a fresh virtual environment"
	@python -m venv venv
	@source venv/bin/activate && make venv-install

venv-install :
	@echo "Install/update required python packages"
	@touch requirements.txt
ifdef VIRTUAL_ENV
	@pip install -r requirements.txt
else
	@echo -e "\e[31mNot in virtual environment"
endif

venv-pack :
	@echo "Update virtual environment requirements"
ifdef VIRTUAL_ENV
	@pip freeze > requirements.txt
else
	@echo -e "\e[31mNot in virtual environment"
endif


# Development management targets
.PHONY : clean test

clean :
	@echo "Deleting all temporary files"
	@find ./ -name "*~" -type f -delete
	@find ./acrome_wrapper -name "__pycache__" -exec rm -r "{}" \;

test :
	@echo "Running unit tests"
	@python test.py


# Packaging management targets
.PHONY : clear build install

clear :
	@echo "Delete compiled package files"
	@rm -fr *.egg-info
	@rm -fr dist

build : clear
	@echo "Building package"
	@source venv/bin/activate && python -m build

install :
	@echo "Installing package locally"
	@pip uninstall --break-system-packages acrome_wrapper
	@pip install -U --break-system-packages dist/*.whl
