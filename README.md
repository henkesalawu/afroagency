# Dancers and Events Agency

## Motivation
This project models a company responsible for managing events and dancers using a Flask API with PostgreSQL and Auth0 for authentication and authorization.

## URL Location
The hosted API URL will be provided once deployed.

## Project Dependencies
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-JWT-Extended
- python-dotenv
- psycopg2-binary
- requests
- auth0-python
- gunicorn

## Local Development
1. **Setup Environment:**
   Create a `.env` file with the following content:
   ```bash
   DATABASE_URL=postgresql://user:password@localhost/dancer_agency
   JWT_SECRET_KEY=your_jwt_secret_key
   AUTH0_DOMAIN=afrodev.uk.auth0.com
   API_IDENTIFIER=https://afrobeatsagency/api
   CLIENT_ID=Qb6zSTa007TeqQA1u4AciCfPeQpnancH
   CLIENT_SECRET=TweVqbFNsgI1CCwUaCgXlMmEtvpQgC18RbwP3j0Z6kwtoRrSUIDX_HeKniAGCDhB
