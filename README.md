# dezentrale
The new Website, based on the dezentrale_web project, but renewed with python3.

To start working on the project, simply clone it via:

`git clone https://github.com/Dezentrale-eV/dezentrale.git` 

*or* via ssh:

`git@github.com:Dezentrale-eV/dezentrale.git`

go into that directory, and install virtualenv via pip3 and activate it:

`pip3 install virtualenv`

`virtualenv .venv`

`source .venv/bin/activate`

To install all dependencies, run `make develop` in that directory (at the same level as manage.py and the Makefile is). 

Note: if an error is occurring, you can download all packages via `pip3 install [package]` on your own, these can be found in the *requirements.txt*.

All you have to do now is to setup the database with the migations, create a superuser and run the development server:

`make migrate`

`make createsuperuser`

`make runserver`
