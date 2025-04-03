import nox
from App.models.db.memcell import memcell
from App.models.db.yamel import Yamel
import tempfile
from pathlib import Path
import subprocess
import time
import requests
import os

# --- GLOBAL CONFIG ---
HOST = 'localhost'
PORT = '8007'
BASE = f'http://localhost:8007'



@nox.session
def test_memcell(session):
    '''
    Manually test memcell creation, conversion, and constraints.
    '''
    try:
        print('\n[TEST] valid memcell')
        mc = memcell(id=1, user='alice@example.com', task='Clean the fridge')
        print(mc)
    except Exception as e:
        print(f'HANDLED: {e}')

    try:
        print('\n[TEST] task too long')
        mc = memcell(id=2, user='bob@example.com', task='a' * 101)
        print(mc)
    except Exception as e:
        print(f'HANDLED: {e}')

    try:
        print('\n[TEST] missing user')
        mc = memcell(id=3, task='No user here')
        print(mc)

    except Exception as e:
        print(f'HANDLED: {e}')

    tests = [
        # valid
        ('Valid memcell from kwargs', lambda: memcell(id=1, user='alice@example.com', task='Feed the dog')),
        
        # valid - from dict
        ('Valid memcell from dict', lambda: memcell({'id': 2, 'user': 'bob@example.com', 'task': 'Buy groceries'})),

        # invalid - task too long
        ('Task too long', lambda: memcell(id=3, user='carol@example.com', task='a' * 101)),

        # invalid - missing id
        ('Missing ID', lambda: memcell(user='dave@example.com', task='Take out trash')),

        # invalid - missing user
        ('Missing user', lambda: memcell(id=4, task='Take out trash')),

        # invalid - missing task
        ('Missing task', lambda: memcell(id=5, user='ellen@example.com')),

        # valid - test __call__ and dict conversion
        ('Dict and call output', lambda: print(dict(memcell(id=6, user='frank@example.com', task='Email client'))))
    ]

    for label, test in tests:
        print(f'\n[TEST] {label}')
        try:
            result = test()
            if isinstance(result, memcell):
                print(result)
            elif isinstance(result, dict):
                print(result)
        except Exception as e:
            print(f'HANDLED: {e}')

@nox.session
def test_yamel(session):
    '''
    Manually test Yamel CRUD and ID logic using a temporary YAML file.
    '''
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / 'memcells.yaml'

        yam = Yamel(path=str(path), tb='memcells', PIN='1010')

        print('\n[CREATE] 3 memcells')
        yam.create('alice@example.com', 'Feed cat')
        yam.create('bob@example.com', 'Fold clothes')
        yam.create('carol@example.com', 'Paint garage')

        print('\n[ALL MEMCELLS]')
        print(yam.all)

        print('\n[DELETE memcell id=2]')
        yam.delete({'id': 2})
        print(yam.all)

    print(f'\n[TEST FILE CLEANED]: {path}')



@nox.session
def integration(session):
    '''
    Launch Flask server and hit endpoints with curl/requests.
    '''
    session.install(".[dev]", "requests")

    server = subprocess.Popen(
        ["python", "-m", "app", "--log", "ERROR"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        start_new_session=True
    )

    try:
        time.sleep(3)  # let the server boot up

        print(f'\n[GET] {BASE}/ping')
        res = requests.get(f'{BASE}/ping')
        print('[RESPONSE]', res.status_code, res.text)

        print(f'\n[POST] {BASE}/memcells')
        payload = {
            'user': 'test@example.com',
            'task': 'Pet the goose'
        }
        res = requests.post(f'{BASE}/memcells', json=payload)
        print('[RESPONSE]', res.status_code, res.json())

        print(f'\n[GET] {BASE}/memcells')
        res = requests.get(f'{BASE}/memcells')
        print('[RESPONSE]', res.status_code)
        for cell in res.json():
            print(' ', cell)

        print(f'\n[DELETE] {BASE}/memcells/1')
        res = requests.delete(f'{BASE}/memcells/1')
        print('[RESPONSE]', res.status_code, res.text)

    finally:
        server.terminate()
        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()
            server.wait()

