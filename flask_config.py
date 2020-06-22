"""Flask configuration class."""
import os

class Config:
    """Base configuration variables."""
    TRELLO_API_KEY = os.environ.get('TRELLO_API_KEY')
    TRELLO_API_TOKEN = os.environ.get('TRELLO_API_TOKEN')

    if not (TRELLO_API_KEY and TRELLO_API_TOKEN):
        raise ValueError("No Trello credentials set for Flask application. Did you forget to run setup.sh?")
