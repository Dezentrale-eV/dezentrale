BUILDDIR ?= _build
ENV ?= dev
PORT ?= 8000
SPHINXOPTS =

define CMDS
ifeq ($(1), runserver)
	dezentrale/manage.py$(1)$(PORT)
else
$(1):
	dezentrale/manage.py$(1)
endif
endef

$(eval $(call CMDS, $(cmd)))

.PHONY: help clean clean-build clean-docs clean-pyc clean-test cmd coverage coverage-html \
    create-db develop docs isort livehtml migrate open-docs runserver shell startapp test \
    test-all test-upload upload

help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  develop                  to install (or update) all packages required for development"
	@echo "  dist                     to package a release"
	@echo "  docs                     to build the project documentation as HTML"
	@echo "  isort                    to run isort on the whole project"
	@echo "  livehtml                 to open documentation in browser and rebuild automatically"
	@echo "  migrate                  to synchronize Django's database state with the current set of models and migrations"
	@echo "  open-docs                to open the project documentation in the default browser"
	@echo "  runserver                to start Django's development Web server"
	@echo "  shell                    to start a Python interactive interpreter"
	@echo "  startapp                 to create a new Django app"
	@echo "  test                     to run unit tests quickly with the default Python"
	@echo "  test-all                 to run unit tests on every Python version with tox"
	@echo "  test-upload              to upload a release to test PyPI using twine"
	@echo "  upload                   to upload a release using twine"
	@echo "  makemigrations			  to create new migrations based on the changes you have made to your models"
	@echo "	 createsuperuser   	      to create a user with admin rights for your local database"
	@echo "	 collectstatic   	      collectstatic"


develop:
	pip3 install -U pip setuptools wheel
	pip3 install -r requirements.txt

dist: clean
	python setup.py sdist bdist_wheel
	ls -l dist

docs:
	$(MAKE) -C docs html BUILDDIR=$(BUILDDIR) SPHINXOPTS='$(SPHINXOPTS)'

isort:
	isort --recursive setup.py dezentrale/ tests/

livehtml: docs
	$(MAKE) -C docs livehtml BUILDDIR=$(BUILDDIR) SPHINXOPTS='$(SPHINXOPTS)'

migrate:
	python3 manage.py migrate

open-docs:
	python3 -c "import os, webbrowser; webbrowser.open('file://{}/docs/{}/html/index.html'.format(os.getcwd(), '$(BUILDDIR)'))"

runserver:
	python3 manage.py runserver $(PORT)

shell:
	python3 manage.py shell

startapp:
	@read -p "Enter the name of the new Django app: " app_name; \
	app_name_title=`python -c "import sys; sys.stdout.write(sys.argv[1].title())" $$app_name`; \
	mkdir -p dezentrale_web/apps/$$app_name; \
	python manage.py startapp $$app_name dezentrale_web/apps/$$app_name --template dezentrale_web/config/app_template; \
	echo "Don't forget to add 'dezentrale.apps."$$app_name".apps."$$app_name_title"Config' to INSTALLED_APPS in 'dezentrale/settings.py'!"

test:
	python3 -m pytest $(TEST_ARGS) tests/

test-all:
	tox

test-upload:
	twine upload -r test -s dist/*
	python -c "import webbrowser; webbrowser.open('https://testpypi.python.org/pypi/dezentrale_web')"

upload:
	twine upload -s dist/*
	python -c "import webbrowser; webbrowser.open('https://pypi.python.org/pypi/dezentrale_web')"

makemigrations:
	python3 manage.py makemigrations

createsuperuser:
	python3 manage.py createsuperuser

collectstatic:
	python3 manage.py collectstatic

# dump local data from sqlite db into json file
# excludes login sessions as well as users.
#
dumpdb:
	python3 manage.py dumpdata --verbosity 3 --indent=2 --exclude=auth.user --exclude=sessions --output fixtures/full.json

# resets database and loads the `full` fixture from the
# `fixtures` folder.
# TODO/tim: Check if we really need a full reset
# I am not sure, if the reset / clean is really the best idea, since `dumpdb` excludes auth.user, we could
# leave everything as it is, but this needs to be tested with additional data being used and potential conflicts.
# For now this should avoid any kind of conflict.
resetdb:
	rm -rf db.sqlite3
	make migrate
	make createsuperuser
	python3 manage.py loaddata --verbosity 3 fixtures/full.json
