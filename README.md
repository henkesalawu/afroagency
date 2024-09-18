# Capstone-Project

This is the final project of Udacity Nanodegree.
The aim of the project is to deploy Flask app on Heroku.
Enable RBA with Auth0.

# Afrobeats Dance Agency

I decided to create the afrobeats dance agency/app.
The idea of the app was to host events. Events' hosts and artists can use it to look for dancers.
App was meant to allow dancers to create their profiles and look for events to perform on.

This project models a website where event hosts and dancers meet. 
Application was created using a Flask API with PostgreSQL.
API is secured using Auth0, and it supports role-based access control (RBAC). The project is hosted live on Heroku.

## Motivation
I love dancing and love afrobeats music and dance. 
This app seem like great idea for dancers, making it easier to find employment and handy for artists and events' hosts looking
for dancers for their events.

I initially created front and backend but was not able to deploy it and use authentication and authorization properly. 
I ended up keeping just backend for this project.
I hope to work on it after the degree and complete the front end as well.

## Project Dependencies

alembic==1.13.2
blinker==1.8.2
click==8.1.7
colorama==0.4.6
ecdsa==0.19.0
Flask==2.3.3
Flask-Login==0.6.3
Flask-Migrate==2.7.0
Flask-Script==2.0.5
Flask-SQLAlchemy==3.1.1
greenlet==3.1.0
gunicorn==23.0.0
importlib_metadata==8.5.0
importlib_resources==6.4.5
itsdangerous==2.2.0
Jinja2==3.1.4
Mako==1.3.5
MarkupSafe==2.1.5
packaging==24.1
psycopg2-binary==2.9.9
pyasn1==0.6.1
python-dotenv==1.0.1
python-jose==3.3.0
rsa==4.9
six==1.16.0
SQLAlchemy==2.0.35
typing_extensions==4.12.2
Werkzeug==3.0.4
zipp==3.20.1

## Local set up
Clone the repository and set up a virtual environment 
```bash
python -m venv venv
source venv/bin/activate  # For Windows use `venv\Scripts\activate`
```

Install project dependencies:

```bash
pip install -r requirements.txt
```

Set up env vari:

$ source setup.sh
$ export FLASK_APP=app.py
$ export FLASK_ENV=development
$ flask run

```bash
export AUTH0_DOMAIN='your-auth0-domain'
export AUTH0_AUDIENCE='your-auth0-audience'
export AUTH0_ALGORITHMS='RS256'
```

Initialize the database:
drop and create db in postgres:

```bash
psql postgres

drop database afrobeatsagency;
create database afrobeatsagency;
\q
```

```bash
flask db init
flask db migrate
flask db upgrade
```
run below to add data to db:
psql testagency < init_data.sql

Run the app:

```bash
flask run
```

This project is hosted live on Heroku.
## URL Location
https://afrobeatsagency-5975d5a5c006.herokuapp.com/

To test endpoints you can execute through CURL or postmand
$ curl -X GET https://harsh-casting-agency.herokuapp.com/dancers
$ curl -X GET https://harsh-casting-agency.herokuapp.com/dancers/1
$ curl -X GET https://harsh-casting-agency.herokuapp.com/events
$ curl -X GET https://harsh-casting-agency.herokuapp.com/events/1
$ curl -X POST https://harsh-casting-agency.herokuapp.com/events
$ curl -X POST https://harsh-casting-agency.herokuapp.com/dancers
$ curl -X PATCH https://harsh-casting-agency.herokuapp.com/dancers/1
$ curl -X DELETE https://harsh-casting-agency.herokuapp.com/events/1

## Hosting Instructions
Install the Heroku CLI.
Login to your Heroku account:

```bash
heroku login
```

Create a new Heroku app:

```bash
heroku create
```

Set up Heroku environment variables:

```bash
heroku config:set AUTH0_DOMAIN='your-auth0-domain'
heroku config:set AUTH0_AUDIENCE='your-auth0-audience'
heroku config:set AUTH0_ALGORITHMS='RS256'
```

Push to Heroku:

```bash
git push heroku main
```

The API implements RBAC to control access to certain endpoints. 
Permissions are a part of JWT tokens
There are 3 roles were defined in Auth0 with following permissions:

DancerAgent
- token : eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjhiQnhKTFF4RFlCeDluWG44d3haRSJ9.eyJpc3MiOiJodHRwczovL2Fmcm9kZXYudWsuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDY2ZThhMmM0NDFiZmQ0M2Q3ZGY1OTUzZSIsImF1ZCI6Imh0dHBzOi8vYWZyb2JlYXRzYWdlbmN5L2FwaSIsImlhdCI6MTcyNjYyOTgwNSwiZXhwIjoxNzI2NjM3MDA1LCJzY29wZSI6IiIsImF6cCI6IlFiNnpTVGEwMDdUZXFRQTF1NEFjaUNmUGVRcG5hbmNIIiwicGVybWlzc2lvbnMiOlsiYWRkOmRhbmNlciIsImRlbGV0ZTpkYW5jZXIiLCJlZGl0OmRhbmNlciIsImdldDpkYW5jZXItZGV0YWlscyJdfQ.LpsixFcOayPM5upnWFndbVbhCAsHaFsOEnph-NlAVfRV_0Gt6a8jNwbcaoSjrxxYT17RgUKxp4CdJ8paTHP34osfuTr6D6F8b11nCUbMbRq1bzCgIu6pggQzkJ_EjB_B8oDzh6sCWE6PJfrVo30CNsRuGDklD9fsP9Kg9-LHUeBIx3RknGRV78bfvKftNARASrzjJIpP6xluw5IhbP5wVrzpBduuc2Wefq-eVXqhM6lz0K0lJXraJXkg0V-aKHKm8Da52i75NUDCChCEwxPntdWj-iltYpEEnG3Ur9vcoi0TGTn1Z1pLaSY7my8iJo_FztE-7fqIPjYlRM82VCB8wA
- permissions:
add:dancer -> Allows adding new dancers
delete:dancer -> Allows deleting dancers
edit:dancer -> Allows editing dancers
get:dancer-details -> Allows viewing detailed information about a specific dancer.

Event User
- token : eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjhiQnhKTFF4RFlCeDluWG44d3haRSJ9.eyJpc3MiOiJodHRwczovL2Fmcm9kZXYudWsuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDY2ZThhMjdhN2M0NGNhYmZmZTM3ZDNjYiIsImF1ZCI6Imh0dHBzOi8vYWZyb2JlYXRzYWdlbmN5L2FwaSIsImlhdCI6MTcyNjYyOTYzNiwiZXhwIjoxNzI2NjM2ODM2LCJzY29wZSI6IiIsImF6cCI6IlFiNnpTVGEwMDdUZXFRQTF1NEFjaUNmUGVRcG5hbmNIIiwicGVybWlzc2lvbnMiOlsiYWRkOmV2ZW50IiwiZGVsZXRlOmV2ZW50IiwiZWRpdDpldmVudCIsImdldDpldmVudC1kZXRhaWxzIl19.eTG0C03ojYf0E6kZiN7jp6lPyngmnEP68ItgZ-z-K5Au2QtAmF55TAPWLX1jWIfJP1lJkEMyqok8gC6u4pMpjlKNj7k5yzsRY2K4L5csCVV_4Lgsw_FskeAuxV4RVR3WC8Sc4nrXMiXIadkrcN6GAxC0Uz4HZjYC9Sz4JXzmCszPrADh00NU0BsKplKzkShMWAeGowppnVR1XjTUTU34ijsBlUM70JmseXiJgheuodiZJvUVY1GgxNrbHluHnn19O3cmll08IL8hfrAl8q8b1OPnMVSbywLYtqaMI6vNdpMkWqxcRQc2tdrK-sZHNE0ksrXGdEynenn7agOy2fTtCQ
- permissions:
add:event -> Allows adding new events
delete:event -> Allows deleting events
edit:event -> Allows editing events
get:event-details -> Allows viewing detailed information about a specific event

Director
-token:eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjhiQnhKTFF4RFlCeDluWG44d3haRSJ9.eyJpc3MiOiJodHRwczovL2Fmcm9kZXYudWsuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDY2ZTlmZTVmMjFjNTFkYWUzMGMyMDIzMyIsImF1ZCI6Imh0dHBzOi8vYWZyb2JlYXRzYWdlbmN5L2FwaSIsImlhdCI6MTcyNjYyOTkxNCwiZXhwIjoxNzI2NjM3MTE0LCJzY29wZSI6IiIsImF6cCI6IlFiNnpTVGEwMDdUZXFRQTF1NEFjaUNmUGVRcG5hbmNIIiwicGVybWlzc2lvbnMiOlsiYWRkOmRhbmNlciIsImFkZDpldmVudCIsImRlbGV0ZTpkYW5jZXIiLCJkZWxldGU6ZXZlbnQiLCJlZGl0OmRhbmNlciIsImVkaXQ6ZXZlbnQiLCJnZXQ6ZGFuY2VyLWRldGFpbHMiLCJnZXQ6ZXZlbnQtZGV0YWlscyJdfQ.koIN7hubpVeeVFhz_uKnP9Lk-LR3JfeWjCx4i9KIZ6fASpR-evE1OCDV6KMv_0ez9nSdqO70OLqmmdKdgtUJ67574SC8gDyGjLtabCQQA0py9MpsFsZvAum8ZR7nL0yDOa38CO_hzx45cAyxbAag-mXDSsLIxAs_wrr8MMX7PPok1QWbybkRnO7WFeVmVmFyc498GdD5ljS-e_wYTCxyM2Jw48WomXAZsuvLbKGenHdk16B16DZpC79ZDLUAjb6SAEyDonsEE0GMlcMkr9VfWiaaukRwYQukWDMV0kzV34jFTYlUqweBttuN217wjBEdt_YezXprh1B87pjPY42jgg
- all permissions

To access protected routes, a valid JWT token must be included in the `Authorization` header as a Bearer token.

## URL Location
https://afrobeatsagency-5975d5a5c006.herokuapp.com/ - display Welcome message
https://afrobeatsagency-5975d5a5c006.herokuapp.com/dancers - display all dancers - results display for all users
https://afrobeatsagency-5975d5a5c006.herokuapp.com/events - display all events - results display for all users

Instructions to check remaining endpoints:

## Models

Dancers and Events

## API Endpoints
GET /dancers
GET /events
GET /dancers/<id>
GET /events/<id>
POST /dancers
POST /events
DELETE /dancers/<id>
DELETE /events/<id>
PATCH /events/<id>
PATCH /dancers/<id>

Examples:

### GET /dancers
Returns a list of all dancers.
Response:
    ```json
    {
        "success": true,
        "dancers": []
    }
    ```

### GET /events
Returns a list of all events.
     ```json
    {
        "success": true,
        "events": []
    }
    ```

### GET /dancers/\<int:id\>
Returns a specific dancer
Permission: get:dancer-details
Response
    ```json
    {
        "success": true,
        "dancer": {
            "id": 1,
            "name": "John Doe",
            "age": 30,
            "gender": "Male",
            "phone": "1234567890",
            "website": "https://example.com"
        }
    }
    ```

### GET /events/\<int:id\>
Returns a specific event
Permission: get:event-details
Response
    ```json
    {
        "success": true,
        "event":  ...
        }
    }
    ```

# DELETE /dancer
Deletes dacncer
Returns success/fail and user id
Permission 'delete:dancer'

# DELETE /event
Deletes devent
Returns success/fail and user id
Permission 'delete:event'

# Edit /events/1
Updates event
Permission: 'edit:event'
returns updated event

# Edit /dancers/1
Updates dancer
Permission: 'edit:dancer'
returns updated dancer

# Add Events
Permission: 'add:event'
returns new event

# Add Dancer
Permission: 'add:dancer'
returns new dancer

Unit tests are provided in `test_app.py`. 
To run the tests

```bash
drop database testagency
create database testagency
psql testagency < init_data.sql
python test_app.py
```

Tests for functionality of the endpoints and the role-based access control.