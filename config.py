import os
from dotenv import load_dotenv
import re

uri = os.getenv("DATABASE_URL")
# or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = uri

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
    API_IDENTIFIER = os.environ.get('API_IDENTIFIER')
    AUTH0_CLIENT_ID = os.environ.get('AUTH0_CLIENT_ID')
    AUTH0_CLIENT_SECRET = os.environ.get('AUTH0_CLIENT_SECRET')
