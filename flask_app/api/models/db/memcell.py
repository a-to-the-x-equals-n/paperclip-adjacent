from typing import Any, Iterator
from collections.abc import Mapping

class memcell(Mapping):
    '''Memcell factory for typecasting-like behavior.'''
    __slots__ = ['id', 'phone', 'task', 'status', '_data']

    def __init__(self, data: dict[str, Any] | None = None, /, *, id: int | None = None, phone: str | None = None, task: str | None = None, status: str = 'pending') -> None:
        '''
        Initialize a memcell from a dictionary or keyword arguments.

        Parameters:
        ----------
        data : dict, optional
            Dictionary containing memcell fields.

        id : int
            Unique ID of the memcell.

        phone : str
            Owner's phone or email.

        task : str
            Task description (max 100 characters).
            
        status : str
            Task status (default: 'pending').
        '''
        if data:
            id = data.get('id')
            phone = data.get('phone')
            task = data.get('task')
            status = data.get('status', 'pending')

        if task and len(task) > 100:
            raise ValueError('Task description exceeds 100 characters.')

        assert id is not None, 'memcell.id cannot be NONE'
        assert phone is not None, 'memcell.phone cannot be NONE'
        assert task is not None, 'memcell.task cannot be NONE'
        
        self.id = id
        self.phone = phone
        self.task = task
        self.status = status

        self._data = {
            'id': self.id,
            'phone': self.phone,
            'task': self.task,
            'status': self.status
        }

    def __repr__(self) -> str:
        '''
        Developer-friendly representation of the memcell.

        Returns:
        -------
        str
            Reconstructable one-liner format.
        '''
        return self.__str__()

    def __str__(self) -> str:
        '''
        Readable formatted view of the memcell.

        Returns:
        -------
        str
            Nicely formatted multiline string.
        '''
        task = self._data['task']
        t = f"{task[:25]}..." if len(task) > 25 else task
        return f"\nmemcell:\n  id: '{self.id}'\n  phone: '{self.phone}'\n  status: '{self.status}'\n  task: '{t}'"

    def __getitem__(self, key: str) -> Any:
        '''
        Retrieve a value by key from the memcell.

        Parameters:
        ----------
        key : str
            The field name to retrieve.

        Returns:
        -------
        Any
            The value associated with the given key.
        '''
        return self._data[key]
    
    def __len__(self) -> int:
        '''
        Return the number of fields in the memcell.

        Returns:
        -------
        int
            The total number of key-value pairs.
        '''
        return len(self._data)
    
    def __iter__(self) -> Iterator[str]:
        '''
        Iterate over the memcell's keys.

        Returns:
        -------
        Iterator
            An iterator over the field names.
        '''
        return iter(self._data)

    def __call__(self) -> dict[str, Any]:
        '''
        Allow direct call to get dict representation.

        Returns:
        -------
        dict
            Dictionary-formatted memcell.
        '''
        return dict(self)

__all__ = ['memcell']

if __name__ == '__main__':
    tests = [
        # valid
        ('Valid memcell from kwargs', lambda: memcell(id=1, phone='alice@example.com', task='Feed the dog')),
        
        # valid - from dict
        ('Valid memcell from dict', lambda: memcell({'id': 2, 'phone': 'bob@example.com', 'task': 'Buy groceries'})),

        # invalid - task too long
        ('Task too long', lambda: memcell(id=3, phone='carol@example.com', task='a' * 101)),

        # invalid - missing id
        ('Missing ID', lambda: memcell(phone='dave@example.com', task='Take out trash')),

        # invalid - missing phone
        ('Missing phone', lambda: memcell(id=4, task='Take out trash')),

        # invalid - missing task
        ('Missing task', lambda: memcell(id=5, phone='ellen@example.com')),

        # valid - test __call__ and dict conversion
        ('Dict and call output', lambda: print(dict(memcell(id=6, phone='frank@example.com', task='Email client'))))
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