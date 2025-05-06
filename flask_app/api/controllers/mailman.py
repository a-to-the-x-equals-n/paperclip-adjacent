from api.utils import Highlander
from api.models import Imap, Smtp
from api.utils.debuggernaut import heimdahl, laufeyspawn, jotunbane
import requests


class Mailman(metaclass = Highlander):
    _COMMANDS = {
        'new', 
        'all', 
        'help',
        'del'
    }

    @laufeyspawn(summoned = True)
    def __init__(self, email: str, pw: str, phone: str, host: str, port: str, table: str):
        self.i = Imap(email, pw, phone)
        self.o = Smtp(email, pw, phone)
        self._URL = f'http://{host}:{port}/{table}'
        self._phone = phone
        self._email = email

        heimdahl(f'[INIT MAILMAN]', unveil = jotunbane, threat = 2)

    @laufeyspawn(summoned = True)
    def start(self):
        while True:
            cmd, content = self.extract(self.i.listen())
            heimdahl(f'[COMMAND] "{cmd}"')
            if cmd not in self.__class__._COMMANDS:
                self.o.malformed()
            self.process(cmd, content = content)

    @laufeyspawn(summoned = True)
    def extract(self, message: str, /, *, content: None = None):
        assert message != '', 'message can\'t be empty'
        assert isinstance(message, str), 'message must be type str'
        assert content is None, 'illegal assignment to `content`'

        cmd = message.strip().lower()
        if ' ' in cmd:
            cmd, content = cmd.split(' ', 1)
        return cmd, content

    @laufeyspawn(summoned = True)
    def process(self, cmd: str, /, *, content: str | None = None):
        match cmd:
            case 'new':
                data = {
                    'phone': self._phone,
                    'task': content
                }
                response = requests.post(self._URL, json = data)
                reply = response.json()
                heimdahl(f'[STATUS] {response.status_code}', unveil = jotunbane, threat = 1)
                heimdahl(f'{reply}', unveil = jotunbane, threat = 1)
                return self.o.new_memcell(reply)

            case 'all':
                response = requests.get(self._URL)
                reply = response.json()
                heimdahl(f'[STATUS] {response.status_code}', unveil = jotunbane, threat = 1)
                heimdahl(f'{reply}', unveil = jotunbane, threat = 1)
                return self.o.all_memcells(reply)
            
            case 'del':
                response = requests.delete(self._URL + f'/{content}')
                try:
                    reply = response.json()
                except:
                    self.o.malformed()
                heimdahl(f'[STATUS] {response.status_code}', unveil = jotunbane, threat = 0)
                heimdahl(f'{reply}', unveil = jotunbane, threat = 1)
                return self.o.del_memcell(reply)

            case 'help':
                return self.o.help()
            
            case _:
                return self.o.malformed()


__all__ = ['Mailman']