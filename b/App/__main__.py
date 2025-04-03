import argparse
from . import init_logs, LOG  # Relative import (since it's inside the package)
from .config import app, IP, PORT
from . import routes

def main():
    parser = argparse.ArgumentParser(description = 'Start backend server.')
    parser.add_argument('--log', '-L', type = str, choices = ['debug', 'info', 'warning', 'error', 'critical'], default = 'debug')
    parser.add_argument('--tail', '-T', action = 'store_true')
    args = parser.parse_args()

    init_logs(args.log, tail = args.tail)
    LOG.info('- SERVER STARTED -')

    app.run(host = IP, port = int(PORT), debug = False, use_reloader = False)


if __name__ == "__main__":
    main()

    '''
    NOTE: EXAMPLE
    =============
    python run.py --log WARNING
    python run.py --tail
    python run.py -L WARNING --tail
    python run.py -L DEBUG
    '''