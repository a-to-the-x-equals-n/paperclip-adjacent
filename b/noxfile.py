import nox
from pathlib import Path

# --- GLOBAL CONFIG ---
HOST = 'localhost'
PORT = '8007'
BASE = f'http://localhost:8007'

@nox.session
def test(session):
    '''
    Run all pytest tests.
    '''
    session.install(".[dev]")
    # Ensure PYTHONPATH includes project root so App/ is importable
    root = Path(__file__).parent.resolve()
    session.env["PYTHONPATH"] = str(root)
    session.run("pytest", "tests")

@nox.session
def test_memcell(session):
    session.install(".[dev]")
    root = Path(__file__).parent.resolve()
    session.env["PYTHONPATH"] = str(root)
    session.run("pytest", "tests/test_memcell.py")

@nox.session
def test_yamel(session):
    session.install(".[dev]")
    root = Path(__file__).parent.resolve()
    session.env["PYTHONPATH"] = str(root)
    session.run("pytest", "tests/test_yamel.py")

@nox.session
def test_routes(session):
    session.install(".[dev]")
    root = Path(__file__).parent.resolve()
    session.env["PYTHONPATH"] = str(root)
    session.run("pytest", "tests/test_routes.py")