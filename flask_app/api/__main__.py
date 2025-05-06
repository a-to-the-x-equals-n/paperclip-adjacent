import argparse
from .config import app, IP, PORT, EMAIL, PW, PHONE, PORT, TABLE
from . import routes
from .utils.debuggernaut import heimdahl
from .controllers import Mailman
import threading
import os

def main():
    parser = argparse.ArgumentParser(description = 'Start backend server.')
    parser.add_argument('-v', action = 'store_true', help = 'verbose/debug mode')
    args = parser.parse_args()
    heimdahl(f'[SERVER ONLINE]', threat = 4)
    app.run(host = IP, port = int(PORT), debug = args.v, use_reloader = True)


if __name__ == '__main__':
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        mailman = Mailman(EMAIL, PW, PHONE, IP, PORT, TABLE)
        threading.Thread(target = mailman.start, daemon = True).start()
    main()