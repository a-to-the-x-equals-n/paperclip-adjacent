from pathlib import Path
from typing import TypeVar, ClassVar, Any
import inspect

_PathLike = TypeVar('_PathLike', str, Path)

class Cache(type):
    '''
    Metaclass that computes (once) and caches the CWD and assigns it to `WHERE_AM_I`.

    This functionality happens 'under-the-hood' prior to any call or invoking of `GoodDog`.
    This ensures `GoodDog.WHERE_AM_I` is populated before any function tries to access it.
    '''
    
    def __new__(cls, name, bases, attrs):
        '''
        Overrides the class creation process to compute and cache the current working directory (CWD).
        
        Parameters:
        -----------
        name : str
            The name of the new class.

        bases : tuple
            The base classes of the new class.

        attrs : dict
            The attributes defined within the new class.

        Returns:
        --------
        type
            A new class with `WHERE_AM_I` set to the computed CWD.
        '''

        attrs['_I_AM_GROOT'] = __name__ == '__main__'

        # returns directory where THIS script is physically located
        # OR returns the directory of the CALLER
        # compute directory--ONCE--at class creation, and store it
        where = attrs['_dir']() if attrs['_I_AM_GROOT'] else attrs['_root_caller_dir']() # call functions directly from GoodDog's attributes dictionary

        # inject 'where' into GoodDog
        attrs['_WHERE_AM_I'] = where
        attrs['where'] = where # workaround to give class level attributes `@property` like behavior
        return super().__new__(cls, name, bases, attrs)

    def __setattr__(cls, name: str, value: Any) -> None:
        '''
        Prevents setting attributes that start with an underscore `_`, ensuring internal attributes remain protected.

        Parameters:
        -----------
        name : str
            The name of the attribute being set.

        value : Any
            The value to assign to the attribute.
        '''
        if name.startswith('_'):
            raise AttributeError((f"\n\n\t\"I'm sorry Dave. I'm afraid I can't do that.\"\n\t\t   - HAL 9000\n"))
        super().__setattr__(name, value)
        
    def __getattribute__(cls, name: str) -> Any:
        '''
        Restricts access to class attributes from outside the class, while allowing magic methods.

        Parameters:
        -----------
        name : str
            The name of the attribute being accessed.

        Returns:
        --------
        Any
            The value of the requested attribute if it's allowed.
        '''

        # allow magic methods like __class__, __module__, etc.
        if name.startswith('__'):
            return super().__getattribute__(name)
        
        

        # check if the call is coming from inside the class
        caller = inspect.stack()[1]
        caller_class = caller.frame.f_locals.get('cls') or caller.frame.f_locals.get('self')

        # explicitly block all attributes that start with '_'
        if caller_class is not cls and name.startswith('_'):
            raise AttributeError(f"\n\n\t\"I'm sorry Dave. I'm afraid I can't let you access '{name}'.\"\n\t\t   - HAL 9000\n")
        return super().__getattribute__(name)

########################
#  - GOODDOG CLASS -   #
########################
class GoodDog(metaclass = Cache):
    _I_AM_GROOT: ClassVar[bool]
    _WHERE_AM_I: ClassVar[_PathLike]

    @staticmethod
    def _dir() -> Path:
        '''
        Returns the absolute path of the current script's directory.

        Returns:
        --------
        Path
            A `Path` object representing the directory path.
        '''
        # returns directory where THIS script is physically located
        dir = Path(__file__).resolve().parent if '__file__' in globals() else Path.cwd()
        return dir

        
    @staticmethod
    def _root_caller_dir()-> Path:
        '''
        Environment agnostic solution to find the directory of the root calling script that initiated execution.

        Returns:
        --------
        Path
            The absolute path of the root calling script’s directory.
        '''
        import sys
        import os

        # special environment handling
        if 'ipykernel' in sys.modules or 'google.colab' in sys.modules:
            return Path.cwd()
        
        # return the directory of the executable (sys.executable)
        if getattr(sys, 'frozen', False):
            return Path(sys.executable).parent

        # directly get `__main__` for normal script execution
        module = sys.modules.get('__main__')
        if hasattr(module, '__file__'):
            return Path(module.__file__).resolve().parent

        # stack inspection for imported modules
        stack = inspect.stack()
        for frame in reversed(stack):                   # search from root outward
            frame_info = inspect.getframeinfo(frame[0]) # metadata about current frame instance
            filename = frame_info.filename              # filename of the script that corresponds to frame instance
            
            # skip internal/virtualenv paths and stdlib
            # filter out system-level files
            # 'site-packages' in filename checks if the script comes from a third-party dependency
            if not filename.startswith(str(Path.cwd())) or 'site-packages' in filename:
                continue # if a script is outside the workspace, it is ignored.
                
            # ensure we're not returning the file where this function is defined
            # ensure the file exists on disk
            if filename != __file__ and os.path.exists(filename):
                return Path(filename).resolve().parent # gets the parent directory, which is the script’s location.

        # fallback for REPL or edge cases
        return Path.cwd()
    
    
    @classmethod
    def _path(cls, file: _PathLike, /, *, dir: _PathLike = None) -> Path:
        '''
        Searches for a file by name recursively from a given directory.

        Parameters:
        -----------
        file : _PathLike
            The name of the file to search for.

        dir : _PathLike, optional
            The directory to start searching from (default: current working directory).

        Returns:
        --------
        Path
            The absolute path of the found file.
        '''
        
        dir = cls._WHERE_AM_I if dir is None else dir

        if isinstance(dir, str):
            dir = Path(dir)

        if isinstance(file, Path):
            file = str(file)
            
        for path in dir.rglob(file):    # recursively searches for the file
            return path.resolve()       # kicks back first match
        
        raise FileNotFoundError(f"\n\n\t\"I'm sorry Dave. I'm afraid I can't find '{file}' in '{dir}'\"\n\t\t   - HAL 9000\n")
    
    
    @classmethod
    def fetch(cls, dir: _PathLike = None, /, *evars: tuple[str, ...]) -> list[str] | str:
        '''
        Loads environment variables from a `.env` file and retrieves specified values.

        Parameters:
        -----------
        dir : _PathLike, optional
            The directory where the `.env` file is located. Defaults to `cls._WHERE_AM_I` if not specified.

        *evars : tuple[str]
            One or more environment variable names to retrieve.

        Returns:
        --------
        list[str] | str
            - If multiple environment variable names are provided, returns a list of values.
            - If a single environment variable name is provided, returns a string.
        '''
        from dotenv import load_dotenv
        from os import getenv

        env = cls._WHERE_AM_I if dir is None else Path(dir) / '.env'

        if not env.exists():
            raise FileNotFoundError(f"\n\n\t\"I'm sorry Dave. I'm afraid I can't find the '{env}' file in '{dir}'.\"\n\t\t - HAL 9000\n")

        try:
            load_dotenv(env)  # cache the `.env` file
        except Exception as e:
            print(f'Error: {str(e)}')
            raise RuntimeError(f"\n\n\t\"I'm sorry Dave. I'm afraid I recieved an error loading the `.env` file.\"\n\t\t - HAL 9000\n")

        # return the requested environment variables
        return [getenv(ev) for ev in evars] if len(evars) > 1 else getenv(evars[0])
    

    @classmethod
    def where_is_it_boy(cls, fpath: _PathLike, /, *, dir: _PathLike = None, mode: str = 'absolute') -> Path:
        '''
        Searches for a file by name within a specified directory and returns its absolute path.

        Parameters:
        -----------
        fpath : _PathLike
            The name of the file to locate.

        dir : _PathLike, optional
            The directory to start searching from.

        Returns:
        --------
        Path
            The absolute path to the located file.

        See Also:
        ---------
        `_path` : 
            The underlying method that finds the absolute path.
        '''
        fpath = cls._path(fpath, dir = dir)
        if mode == 'absolute':
            return fpath
        if mode == 'parent':
            return fpath.parent