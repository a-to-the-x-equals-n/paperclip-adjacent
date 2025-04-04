import subprocess
import requests
import time
from pathlib import Path
import tempfile
import os

BASE = 'http://localhost:8007'

def wait_for_server():
    for _ in range(10):
        try:
            res = requests.get(f'{BASE}/ping')
            if res.status_code == 200:
                return True
        except Exception:
            time.sleep(0.5)
    return False

def test_integration_flask_endpoints():
    root_dir = Path(__file__).resolve().parent.parent  # project root

    # create a temporary YAML file
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as tmpfile:
        yaml_path = tmpfile.name

    # set env var so App/config.py can pick it up
    env = os.environ.copy()
    env["DB_PATH"] = yaml_path

    server = subprocess.Popen(
        ["python", "-m", "App", "--log", "error"],
        cwd=root_dir,
        env=env,  # pass env with DB_PATH override
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        start_new_session=True
    )

    try:
        assert wait_for_server(), 'Server did not boot up'

        res = requests.get(f'{BASE}/ping')
        assert res.status_code == 200
        assert res.json().get('message') == 'pong'

        payload = {'user': 'test@example.com', 'task': 'Pet the goose'}
        res = requests.post(f'{BASE}/memcells', json=payload)
        print("CREATE RESPONSE BODY:\n", res.text)
        assert res.status_code == 201
        doc_id = res.json().get('doc_id')
        assert doc_id is not None

        res = requests.get(f'{BASE}/memcells')
        assert res.status_code == 200
        assert any(cell['id'] == doc_id for cell in res.json())

        res = requests.delete(f'{BASE}/memcells/{doc_id}')
        assert res.status_code == 200
        assert res.json().get('deleted') == [doc_id]

    finally:
        server.terminate()
        try:
            out, err = server.communicate(timeout=5)
            print("STDERR:\n", err.decode())
            print("STDOUT:\n", out.decode())
        except subprocess.TimeoutExpired:
            server.kill()
            out, err = server.communicate()
            print("SERVER TIMED OUT")
            print("STDERR:\n", err.decode())
            print("STDOUT:\n", out.decode())
        finally:
            os.remove(yaml_path)  # clean up temp file