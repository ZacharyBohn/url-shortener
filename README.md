# URL Shortener

A system that will shorten long urls to shorter ones

## Getting started

### Setting up the database

Create a Dynamo database in AWS and name it `shorten_urls`

[link to Dynamo](https://aws.amazon.com/dynamodb/)

Then create two environment variables named on your machine

`AWS_ACCESS_KEY_ID`

`AWS_SECRET_ACCESS_KEY`

and set their values to the values provided by AWS.

### Windows

In the project folder run

`python -m venv env`

which creates a virtual environment

`env\Scripts\activate`

activates the virtual environment.

`pip install -r requirements.txt`

installs requirements into the virutal environment.

`uvicorn main:app`

launches the app.

`curl localhost:8000/ping`

tests an endpoint on the app. should return "ok".

### Linux / Macos

In the project folder run

`python -m venv env`

which creates a virtual environment

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

## Examples

Examples of curl commands to access this application can be [found here](EXAMPLES.md)