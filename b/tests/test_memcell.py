import pytest
from App.models.db.memcell import memcell

@pytest.mark.parametrize("label, builder", [
    ('Valid memcell from kwargs', lambda: memcell(id=1, user='alice@example.com', task='Feed the dog')),
    ('Valid memcell from dict', lambda: memcell({'id': 2, 'user': 'bob@example.com', 'task': 'Buy groceries'})),
    ('Task too long', lambda: memcell(id=3, user='carol@example.com', task='a' * 101)),
    ('Missing ID', lambda: memcell(user='dave@example.com', task='Take out trash')),
    ('Missing user', lambda: memcell(id=4, task='Take out trash')),
    ('Missing task', lambda: memcell(id=5, user='ellen@example.com')),
])
def test_memcell_cases(label, builder):
    if "Missing" in label or "too long" in label:
        with pytest.raises(Exception):
            builder()
    else:
        cell = builder()
        assert isinstance(cell, memcell)

def test_memcell_dict_conversion():
    cell = memcell(id=6, user='frank@example.com', task='Email client')
    result = dict(cell)
    assert result['task'] == 'Email client'