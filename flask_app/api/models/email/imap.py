import imaplib
import time
import email
from api.utils import Highlander
from api.utils.debuggernaut import heimdahl, laufeyspawn, jotunbane

class Imap:
    __slots__ = ['_email_addr', '_mail', '_num', '_sender']

    _IMAP_SERVER = 'imap.gmail.com'
    _GATEWAY = '@vtext.com'
    _FOLDER = 'inbox'

    @laufeyspawn(summoned = True)
    def __init__(self, addr: str, pw: str, number: str | int) -> None:
        self._email_addr = addr
        self._num = str(number)
        self._mail = imaplib.IMAP4_SSL(self.__class__._IMAP_SERVER)
        self._mail.login(self._email_addr, pw)
        self._mail.select(self.__class__._FOLDER)
        self._sender = f'{self._num}{self.__class__._GATEWAY}'
        heimdahl(f'[INIT IMAP]', unveil = jotunbane, threat = 2)

    @laufeyspawn(summoned = True)
    def listen(self):
        heimdahl(f'[LISTENING]', unveil = jotunbane, threat = 3)
        while True:
            self._mail.noop()
            # search the inbox for unread messages from the expected gateway address
            # this returns message ids assigned by the imap server for this mailbox session
            status, msg_ids = self._mail.search(None, f'(UNSEEN FROM "{self._sender}")')

            # guard against bad status or no message IDs returned
            if status != 'OK' or not msg_ids or not msg_ids[0].strip():
                heimdahl(f'[NO MESSAGES]', unveil = False, threat = 3)
                time.sleep(1)
                continue
            
            # msg_ids[0] is a space-separated byte string of message ids
            # - each id represents a specific message in the currently selected mailbox (inbox)
            email_ids = msg_ids[0].split()

            for eid in email_ids:
                # fetch full raw email content for given message id
                # the id is passed as a byte string 
                status, b_msg = self._mail.fetch(eid, '(RFC822)')
                if status != 'OK':
                    heimdahl(f'[ID FETCH FAIL] {eid}', unveil = jotunbane, threat = 3)
                    continue

                for response in b_msg:
                    if isinstance(response, tuple):
                        # parse raw email bytes -> structured email message object
                        msg = email.message_from_bytes(response[1])
                        heimdahl(f'[FROM] {self._sender}', unveil = jotunbane)
                        
                        # extract plain text body from the email
                        if msg.is_multipart():
                            # multipart messages have several content blocks 
                            # (plain text, html, attachments)
                            for part in msg.walk():
                                t = part.get_content_type()
                                if t == 'text/plain':
                                    body = part.get_payload(decode = True).decode(part.get_content_charset() or 'utf-8', errors = 'replace')
                                    heimdahl(f'[BODY] "{body.strip()}"', unveil = jotunbane, threat = 1)
                                    self._mail.store(eid, '+FLAGS', '\\Seen')
                                    return body
                        else:
                            # non-multipart messages have a single payload
                            body = msg.get_payload(decode = True).decode(msg.get_content_charset() or 'utf-8', errors = 'replace')
                            heimdahl(f'[BODY] "{body.strip()}"', unveil = jotunbane, threat = 1)
                            self._mail.store(eid, '+FLAGS', '\\Seen')
                            return body
            time.sleep(1)

    @laufeyspawn(summoned = False)
    def update(self):
        # search the inbox for unread messages from the expected gateway address
        # this returns message ids assigned by the imap server for this mailbox session
        status, msg_ids = self._mail.search(None, f'(UNSEEN FROM "{self._sender}")')
        
        # msg_ids[0] is a space-separated byte string of message ids
        # - each id represents a specific message in the currently selected mailbox (inbox)
        email_ids = msg_ids[0].split()

        for eid in email_ids:
            # fetch full raw email content for given message id
            # the id is passed as a byte string 
            status, b_msg = self._mail.fetch(eid, '(RFC822)')
            if status != 'OK':
                heimdahl(f'[ID FETCH FAIL] {eid}', unveil = jotunbane, threat = 3)
                return None

            for response in b_msg:
                if isinstance(response, tuple):
                    # parse raw email bytes -> structured email message object
                    msg = email.message_from_bytes(response[1])
                    heimdahl(f'[FROM] {self._sender}', unveil = jotunbane)

                    # extract plain text body 
                    if msg.is_multipart():
                        # multipart messages have several content blocks 
                        # (plain text, html, attachments)
                        for part in msg.walk():
                            t = part.get_content_type()
                            if t == 'text/plain':
                                body = part.get_payload(decode = True).decode()
                                heimdahl(f'[BODY] {body}', unveil = jotunbane, threat = 1)
                                return body
                    else:
                        # non-multipart messages -> single payload
                        body = msg.get_payload(decode = True).decode()
                        heimdahl(f'[BODY] {body}', unveil = jotunbane, threat = 1)
                        return body


__all__ = ['Imap']