import yaml
from tinydb.storages import Storage

class YStorage(Storage):
    '''
    TinyDB-compatible storage that reads/writes YAML.
    '''
    __slots__ = ['_path']
    
    def __init__(self, path: str):
        self._path = path

    # --- STORAGE INTERFACE ---

    def read(self) -> dict[str, object]:
        '''
        Read and load YAML content into TinyDB format.

        Returns:
        -------
        dict
            Parsed database content or empty dict.
        '''
        try:
            with open(self._path, 'r') as f:
                return yaml.safe_load(f) or {}
        except FileNotFoundError:
            # return {}
            raise FileNotFoundError(f'filepath: {self._path}')

    def write(self, data: dict[str, object]) -> None:
        '''
        Write database content to YAML file.

        Parameters:
        ----------
        data : dict
            Database data to write.
        '''
        with open(self._path, 'w') as f:
            yaml.dump(data, f)

    def close(self) -> None:
        '''
        Close the storage (noop for YAML).
        '''
        pass
