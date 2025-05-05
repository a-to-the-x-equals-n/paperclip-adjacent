import threading

class Highlander(type):
    '''
    There can be only one... 
    
    Thread-safe singleton metaclass
    '''
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
    
__all__ = ['Highlander']