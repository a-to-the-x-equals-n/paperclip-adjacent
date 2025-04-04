import nox
from pathlib import Path

# --- GLOBAL CONFIG ---

HOST = 'localhost'
PORT = '8007'
BASE = f'http://{HOST}:{PORT}'
DIR = Path("tests/results")


def _prepare_env(session):
    session.install(".[dev]")
    root = Path(__file__).parent.resolve()
    session.env["PYTHONPATH"] = str(root)
    DIR.mkdir(parents = True, exist_ok = True)


@nox.session
def test(session):
    '''
    Run all tests and export results as JUnit XML (for Jenkins).
    '''
    _prepare_env(session)
    
    # use pytest config from pyproject.toml
    session.run("pytest")


@nox.session
def test_memcell(session):
    '''
    Run only memcell tests.
    '''
    _prepare_env(session)
    session.run("pytest", "tests/test_memcell.py", "--junit-xml=tests/results/memcell.xml")


@nox.session
def test_yamel(session):
    '''
    Run only Yamel tests.
    '''
    _prepare_env(session)
    session.run("pytest", "tests/test_yamel.py", "--junit-xml=tests/results/yamel.xml")


@nox.session
def test_routes(session):
    '''
    Run only integration tests for Flask routes.
    '''
    _prepare_env(session)
    session.run("pytest", "tests/test_routes.py", "--junit-xml=tests/results/routes.xml")
