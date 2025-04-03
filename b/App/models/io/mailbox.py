from ..email.imap import IMAP
from typing import Any, List
import email


class Mailbox:

    __slots__ = ['_reader', '_instance']
    _instance: 'Mailbox' | None = None # single instance

    # singleton
    def __new__(cls, *args: Any, **kwargs: Any) -> 'Mailbox':
        if cls._instance is None:
            cls._instance = super(IMAP, cls).__new__(cls)
        return cls._instance


    def __init__(self) -> None:
        self._scan: IMAP = IMAP()


    def scan_inbox(self, users: List[str]) -> None:
        ''' Scans email for any new messages '''
        [self.__scan_for_unread_emails(user) for user in users]


    def __scan_for_unread_emails(self, user):
        sms_list = [] # hold text messages

        status, msg = self._scan.search(None, f'FROM "{user["phone"]}" UNSEEN')

        if status == "OK" and msg[0].split():
            user["sms"] = msg

            for email_msg_id in user['sms'][0].split():
                _, msg_data = self._scan.fetch(email_msg_id, "(RFC822)")
                msg = email.message_from_bytes(msg_data[0][1])

                # Extract the SMS content from the email
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain": # extract plain text only
                            body = part.get_payload(decode = True).decode()
                            self._scan.store(email_msg_id, '+FLAGS', '\\Seen') # mark as read
                            sms_list.append(Mailbox.__extract_text_message(body)) # add sms content to list
                else:
                    body = msg.get_payload(decode = True).decode()
                    self._scan.store(email_msg_id, '+FLAGS', '\\Seen')  # mark as read
                    sms_list.append(Mailbox.__extract_text_message(body))  # add sms content to list

        # TODO: pass into queue to process the outgoing messages


    def __extract_text_message(self, body: str):
        cutoff_phrases = [
            "YOUR ACCOUNT",
            "To respond to this text message, reply to this email or visit Google Voice."
            ]

        # Find the first occurrence of a cutoff phrase
        end = len(body)
        for phrase in cutoff_phrases:
            position = body.find(phrase)
            if position != -1 and position < end:
                end = position

        return body[28:end].strip()

