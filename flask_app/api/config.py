from flask import Flask
from flask_cors import CORS
from .utils import GoodDog as dog
from .models.db import Yamel
from pathlib import Path

try:
    EMAIL, PW, PHONE, IP, PORT, TABLE, PATH = dog.fetch(
        dog.where, 'EMAIL', 'PASSWORD', 'PHONE', 'IP', 'PORT', 'TABLE', 'DB_PATH'
    )
except FileNotFoundError:
    try:
        dir = dog.where_is_it_boy('.env', mode = 'parent')
        EMAIL, PW, PHONE, IP, PORT, TABLE, PATH = dog.fetch(
            dog.where, 'EMAIL', 'PASSWORD', 'PHONE', 'IP', 'PORT', 'TABLE', 'DB_PATH'
        )
    except FileNotFoundError:
        dir = Path.cwd() / Path('api')
        EMAIL, PW, PHONE, IP, PORT, TABLE, PATH = dog.fetch(
            dir, 'EMAIL', 'PASSWORD', 'PHONE', 'IP', 'PORT', 'TABLE', 'DB_PATH'
        )
        
    
PATH = dog.where_is_it_boy(PATH)
db = Yamel(path = PATH, tb = TABLE)
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
app.config['JSON_AS_ASCII'] = False

CORS(app) 