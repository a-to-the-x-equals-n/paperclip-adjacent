import pytest
from pathlib import Path
import tempfile
from App.models.db.yamel import Yamel

@pytest.fixture
def temp_yamel():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "memcells.yaml"
        yield Yamel(path=str(path), tb="memcells", PIN="1010")

def test_yamel_create_and_delete(temp_yamel):
    yam = temp_yamel

    # Create 3 memcells
    yam.create('alice@example.com', 'Feed cat')
    yam.create('bob@example.com', 'Fold clothes')
    yam.create('carol@example.com', 'Paint garage')

    all_cells = yam.all
    assert len(all_cells) == 3

    # Delete one
    deleted = yam.delete({'id': 2})
    assert isinstance(deleted, list)
    assert len(deleted) == 1
    assert 2 in deleted

    after_delete = yam.all
    assert all(cell['id'] != 2 for cell in after_delete)
