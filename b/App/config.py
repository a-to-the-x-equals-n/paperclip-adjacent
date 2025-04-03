from flask import Flask
from flask_cors import CORS
from .helpers.goodboy import GoodDog as dog
from .models.db.yamel import Yamel
from pathlib import Path
from App import LOG

try:
    EMAIL, PW, PHONE, IP, PORT, PIN, TABLE, PATH = dog.fetch(
        dog.where, 'MAIL', 'PW', 'PHONE', 'IP', 'PORT', 'PIN', 'TABLE', 'DB_PATH'
    )
except FileNotFoundError:
    try:
        dir = dog.where_is_it_boy('.env', mode = 'parent')
        EMAIL, PW, PHONE, IP, PORT, PIN, TABLE, PATH = dog.fetch(
            dog.where, 'MAIL', 'PW', 'PHONE', 'IP', 'PORT', 'PIN', 'TABLE', 'DB_PATH'
        )
    except FileNotFoundError:
        dir = Path.cwd() / Path('App')
        EMAIL, PW, PHONE, IP, PORT, PIN, TABLE, PATH = dog.fetch(
            dir, 'MAIL', 'PW', 'PHONE', 'IP', 'PORT', 'PIN', 'TABLE', 'DB_PATH'
        )
        

db = Yamel(path = PATH, tb = TABLE, PIN = PIN)
app = Flask(__name__)
CORS(app) 


'''
NOTE: LOG EXAMPLES
------------------
LOG.debug('This is a debug message')
LOG.info('User requested all memcells')
LOG.warning('Could not find memcell with id = 3')
LOG.error('Something went wrong')
LOG.critical('Database completely unavailable')
'''