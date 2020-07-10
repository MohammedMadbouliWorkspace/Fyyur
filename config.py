import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# This is a postgresql database public uri for testing app immediately
SQLALCHEMY_DATABASE_URI = 'postgres://fyyur@dbhost.fyyur.ml:5432/fyyur'
