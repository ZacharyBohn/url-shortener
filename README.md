# URL Shortener

A system that will shorten long urls to shorter ones

## Getting started

### Windows

In the project folder run

`env\Scripts\activate`

activates the virtual environment.

`pip install -r requirements.txt`

installs requirements.

`uvicorn main:app`

launches the app.

`curl localhost:8000/ping`

tests an endpoint on the app. should return "ok".

### Linux / Macos

In the project folder run

`source env/bin/activate`

activates the virtual environment.

`pip install -r requirements.txt`

installs requirements.

`uvicorn main:app`

launches the app.

`curl localhost:8000/ping`

tests an endpoint on the app. should return "ok".

## Running the application

You can run the application in dev mode with

`uvicorn main:app --reload`

or run it in production mode with

`uvicorn main:app`

## Tests

You can run all the tests with

`python test.py`

This service is mocked using moto, so all tests can be run locally.