from tinydb import TinyDB, Query
from tinydb.queries import QueryInstance
from .ystore import YStorage
from .memcell import memcell
from .singlemeta import Highlander

class Yamel(metaclass = Highlander):
    
    __slots__ = ('_db', '_query', '_ids', '_PIN')

    _MAX_CELLS = 10

    def __init__(self, /, *, path: str | None = None, tb : str | None = None, PIN: str | None = None) -> None:
        '''
        Initialize the TinyDB instance with YAML storage.

        Parameters:
        ----------
        path : str
            Path to the YAML database file.
        '''
        assert PIN is not None, 'PIN cannot be NONE'
        assert tb is not None, 'tb cannot be None'
        assert path is not None, 'path cannot be None'

        db = TinyDB(path, storage = YStorage)
        self._db = db.table(tb)
        self._query = Query()
        self._ids = self._available_ids()
        self._PIN = PIN

    @property
    def next_id(self) -> int:
        '''
        Get the next available ID.

        Returns:
        -------
        int
            Next ID from the available list.
        '''
        if not self._available_ids():
            return -1
        
        try:
            return self._ids.pop(0)
        except IndexError:
            return 1
    
    def _available_ids(self) -> list[int]:
        '''
        Find all unused IDs from 1 to cls._max_cells.

        Returns:
        --------
        list[int]
            Sorted list of available IDs.
        '''
        used = {cell['id'] for cell in self.all if 'id' in cell}
        return sorted([i for i in range(1, self.__class__._MAX_CELLS + 1) if i not in used])

    # --- CRUD OPERATIONS ---

    def clear(self) -> None:
        '''
        Prompt for a 4-digit PIN before wiping all records from the database.

        If the PIN is incorrect or cancelled, no action is taken.
        '''
        pin = input('Enter PIN to confirm database wipe: ').strip()

        if not pin.isdigit() or len(pin) != 4:
            return print('[ABORTING]')

        if pin != self._PIN:
            return print('[ABORTING]')
            
        self._db.truncate()
        print('[DELETED]')

    @property
    def all(self) -> list[dict[str, object]]:
        '''
        Fetch all records from the database.

        Returns:
        -------
        list
            All stored records.
        '''
        results = self._db.all()
        return [memcell(doc) for doc in results]
    
    def create(self, user: str, task: str) -> int | str:
        '''
        Create a memcell with auto-assigned ID from available pool.

        Parameters:
        ----------
        user : str
            Owner of the task.

        task : str
            Task description.

        Returns:
        --------
        int
            TinyDB internal document ID.
        '''
        mem_id = self.next_id
        if mem_id < 0:
            raise RuntimeError('No memcell slots available (max = 10).')

        cell = memcell(id = mem_id, user = user, task = task, status = 'pending')
        return self._db.insert(cell)

    def where(self, filters: dict[str, object]) -> list[dict[str, object]]:
        '''
        Fetch records that match given filters.

        Parameters:
        ----------
        filters : dict
            Field-value pairs to match.

        Returns:
        -------
        list
            Matching records.
        '''
        q = self._build_query(filters)
        results = self._db.search(q)
        return [memcell(doc) for doc in results]

    def update(self, updates: dict[str, object], filters: dict[str, object]) -> int:
        '''
        Update matching records with new data.

        Parameters:
        ----------
        updates : dict
            Fields and values to update.

        filters : dict
            Conditions to select records.

        Returns:
        -------
        int
            Number of records updated.
        '''
        q = self._build_query(filters)
        return self._db.update(updates, q)

    def delete(self, filters: dict[str, object]) -> int:
        '''
        Delete memcells matching filters and reclaim their IDs.

        Parameters:
        ----------
        filters : dict
            Conditions to match records.

        Returns:
        -------
        int
            Number of records deleted.
        '''
        matching = self.where(filters)
        for cell in matching:
            if 'id' in cell:
                self._ids.append(cell['id'])

        self._ids.sort()
        q = self._build_query(filters)
        return self._db.remove(q)
    
    # --- QUERY BUILD HELPER ---

    def _build_query(self, filters: dict[str, object]) -> QueryInstance:
        '''
        Build a TinyDB query from filter conditions.

        Parameters:
        ----------
        filters : dict
            Field-value pairs to match.

        Returns:
        -------
        Query
            Combined query object.
        '''
        q = None
        for k, v in filters.items():
            condition = (self._query[k] == v)
            q = condition if q is None else q & condition
        return q



if __name__ == '__main__':
    yam = Yamel()

    yam.clear()
    # 1. Create three new memcells
    yam.create('alice@example.com', 'Water the plants')
    yam.create('bob@example.com', 'Read Dune')
    yam.create('carol@example.com', 'Fix the bike')

    # 2. Output all memcells
    print('\n[ALL MEMCELLS]')
    print(yam.all)

    # 3. Delete memcell with id = 2
    deleted = yam.delete({'id': 2})
    print(f'\n[DELETE] Removed {deleted} memcell(s) with id=2')

    # 4. Output all memcells again
    print('\n[AFTER DELETE]')
    print(yam.all)
