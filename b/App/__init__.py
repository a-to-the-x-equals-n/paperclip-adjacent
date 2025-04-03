import logging              # for printing messages to console or file

'''
levels = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}
'''

# this will be set by __main__.py
LOG = logging.getLogger(__name__)

def init_logs(level: str = 'DEBUG', tail: bool = False) -> None:
    '''
    Sets up global logging using the provided log level string.
    Always writes logs to a file. Optionally prints to terminal if tail=True.

    Parameters:
    -----------
    level : str
        Expected values like 'DEBUG', 'INFO', 'WARNING', etc.

    tail : bool
        If True, logs will also stream to the terminal in addition to the log file.
    '''

    # convert the input string 'level' to logging level constant
    # if the name doesn't exist/typo, fallback to logging.DEBUG
    level = getattr(logging, level.upper(), logging.DEBUG)


    # create file handler to log into 'app.log'
    file_handler = logging.FileHandler(f'app.log')
    file_handler.setLevel(level)

    # format used by both handlers
    formatter = logging.Formatter(
        fmt = '%(asctime)s | %(levelname)s | %(name)s - %(message)s',
        datefmt = '%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    handlers = [file_handler]


    # optionally add a stream handler
    if tail:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(level)
        stream_handler.setFormatter(formatter)
        handlers.append(stream_handler)

    # apply the handlers
    logging.basicConfig(level = level, handlers = handlers)
    LOG.setLevel(level)
    LOG.debug(f'Logger initialized. level = {level}, tail = {tail}')