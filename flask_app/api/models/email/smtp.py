from email.mime.text import MIMEText
import smtplib
from api.utils import Highlander
from api.utils.debuggernaut import laufeyspawn, heimdahl, jotunbane

class Smtp:
    _PORT = 587
    _SMTP = 'smtp.gmail.com'
    _GATEWAY_MMS = '@vzwpix.com'
    _GATEWAY = '@vtext.com'
    _SMS_MAX_LENGTH = 160

    @laufeyspawn(summoned = False)
    def __init__(self, email: str, pw: str, phone: str):
        self._email = email
        self._pw = pw
        self._phone = phone
        heimdahl(f'[INIT SMTP]', unveil = jotunbane, threat = 2)

    @laufeyspawn(summoned = True)
    def new_memcell(self, reply: dict):
        '''
        EXAMPLE
        =======
        {
            "created": {
                "id": 1,
                "task": "dummy tester"
            }
        }
        '''
        if 'created' not in reply:
            return self.malformed()
        
        reply = reply['created']
        body = (
            f"[NEW MEMCELL]"
            f'\n - task: "{reply["task"][:30]}"'
            f"\n - ID: {reply['id']}"
        )
        self.send(body)

    @laufeyspawn(summoned = True)
    def all_memcells(self, reply: dict | list):
        '''
        EXAMPLE
        =======
        [
            {
                "id": 1,
                "phone": "9104592653",
                "status": "pending",
                "task": "dummy tester"
            },
            {
                "id": 2,
                "phone": "9104592653",
                "status": "pending",
                "task": "dummy tester"
            }
        ]
        '''
        body = '[ALL]'
        if not reply:
            body += f'''\nYou currently have no memcells being tracked.'''
        else:
            for doc in reply:
                body += f'''\n - id: {doc['id']}\n - task: {doc['task']}'''
        
        self.send(body)
    
    @laufeyspawn(summoned = True)
    def del_memcell(self, reply: dict):
        '''
        EXAMPLE
        =======
        {
            "deleted": {
                "id": 1,
                "task": "dummy tester"
            }
        }
        '''
        if 'deleted' not in reply:
            return self.malformed()

        reply = reply['deleted']
        body = (
            f'[DEL MEMCELL]'
            f'\n - task: "{reply["task"][:30]}"'
            f'\n - ID: {reply["id"]}'
        )
        self.send(body)

    @laufeyspawn(summoned = True)
    def help(self):
        body = (
            "[HELP]\n"
            " - 'del' followed by a task ID will remove it.\n"
            " - 'new' then a description will create a task.\n"
            " - 'all' will return all current tasks.\n"
            " - 'help' will return all valid commands."
        )
        self.send(body)

    @laufeyspawn(summoned = True)
    def malformed(self):
        body = (
            "[UNRECOGNIZED COMMAND]\n"
            " - 'del' followed by a task ID will remove it.\n"
            " - 'new' then a description will create a task.\n"
            " - 'all' will return all current tasks.\n"
            " - 'help' will return all valid commands."
        )
        self.send(body)

    @laufeyspawn(summoned = True)
    def send(self, body: str):
        mail_to = f'{self._phone}{self.__class__._GATEWAY_MMS}'
        msg = MIMEText(body, _subtype = 'plain', _charset = 'utf-8')
        msg['From'] = self._email
        msg['To'] = mail_to

        try:
            # connect to the SMTP server and send the email
            server = smtplib.SMTP(self.__class__._SMTP, self.__class__._PORT)
            server.starttls()
            server.login(self._email, self._pw)
            server.sendmail(self._email, mail_to, msg.as_string())
            server.quit()

            heimdahl('[SMS SENT]', unveil = jotunbane, threat = 1)

        except Exception as e:
            heimdahl(f'[SMS FAIL] {e}', unveil = True, threat = 3)


__all__ = ['Smtp']