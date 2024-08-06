# URL Shortener

A system that will shorten long urls to shorter ones

## Getting started

### Windows

In the project folder run

`python -m venv env`

`env\Scripts\activate`

`pip install -r requirements.txt`

### Linux / Macos

In the project folder run

`python -m venv env`

`source env/bin/activate`

`pip install -r requirements.txt`

### Running the application

You can run the application in dev mode with

`fastapi dev main.py`

or run it in production mode with

`fastapi run`

### Tests

You can run all the tests with

`python tests.py`

The only outside service needed to run the tests is AWS' dynamoDB.

This service is mocked using moto, so all tests can be run locally.