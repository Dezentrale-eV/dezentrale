# dezentrale Website
The new Website, based on the dezentrale_web project, but renewed with python3.

## Setup

To start working on the project, simply clone it via:

```bash
git clone https://github.com/Dezentrale-eV/dezentrale.git
``` 

*or* via ssh:

```bash
git@github.com:Dezentrale-eV/dezentrale.git
```

go into that directory, and install virtualenv via pip3 and activate it:

```
pip3 install virtualenv
virtualenv .venv
source .venv/bin/activate
```

To install all dependencies, run the respective make target in the main directory:
 
 ```bash
 make develop
 ``` 

Note: if an error is occurring, you can download all packages manually via pip:

```bash
pip3 install -r requirements.txt
```

All you have to do now is to setup the database with the migations and create a superuser:

```bash
make migrate
make createsuperuser
```

## Development
To run the development server, run the respective make target:

```bash
make runserver
```

### Dumping the database to a fixture
To dump the whole sqlite database (path: `db.sqlite3`), you can use the following make target:

```bash
make dumpdb
```

Note: this dump excludes all existing sessions as well as all backend/frontend users.

### Resetting / initializing the database
To reset and re-initialize the database from the `full.json` fixture, you can run the following make target:
```bash
make resetdb
```

Note: Handle with care!
This *wipes* the whole database and re-initializes it, asks for creating your superuser again and then
applies the fixture from `fixtures/full.json` which is usually created by calling `make dumpdb`.