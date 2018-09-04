# Flask_Template  

A simple boilerplate template to get started with a Flask web application.  

## Installation  

* Install the virtual environment: `virtualenv venv`  
* Activate the virtual environment: `source venv/bin/activate`  
* Install required modules: `pip install -r requirements.txt`  

## First DB migration  

The first time the database is created, the `db_repo` directory is created; it will contain details for the database versioning system, as provided by the `sqlalchemy-migrate` module.  

* Create the database: `python db_create.py`  
* Perform the first migration: `python db_migrate.py`  

For subsequent migrations, only the `python db_migrate.py` is needed.  

## Running the DB  
With the command `python run.py` the database and its web interface will be served on `120.0.0.1:5000`.    

When finished, deactivate the virtual environment: `deactivate`.  

