import imaplib
from ..shield.vault import Vault
import time


class IMAP:

    """
        IMAP_Mgr is a manager class responsible for handling IMAP email connections. It ensures that
        no more than 5 IMAP connections are active at any given time and manages the connection lifecycle.

        The class uses the `Vault` class to securely handle login credentials, and it maintains
        a count of active connections to prevent overloading the IMAP server with too many simultaneous
        connections.

        Attributes:
        ----------
        module : str
            The name of the module used for IMAP connections, set to 'imaplib'.

        connections : int
            A class-level attribute that tracks the number of active IMAP connections.

        imap : imaplib.IMAP4_SSL
            An instance of the IMAP4_SSL class from the `imaplib` module used to establish secure
            IMAP connections.

        passkey : Vault
            An instance of the `Vault` class used to securely manage and retrieve login credentials.

        Methods:
        -------
        __init__(self) -> None:
            Initializes an IMAP connection, ensuring that the number of active connections does not
            exceed 5. Uses the `Vault` instance to securely log in to the IMAP server.

        __add_connection(cls) -> None:
            A class method that increments the `connections` count, ensuring accurate tracking of
            active connections.

        __del__(self) -> None:
            Decrements the `connections` count when an instance of `IMAP_Mgr` is deleted, ensuring
            that the connection count accurately reflects active connections.
        """

    __slots__ = []

    module: str = 'imaplib'
    connections: int = 0
    imap: imaplib.IMAP4_SSL = imaplib.IMAP4_SSL("imap.gmail.com")
    passkey: Vault = Vault()

    def __init__(self) -> None:
        # Ensure that no more than 5 connections are active at once
        while IMAP.connections > 5:
            time.sleep(1)

        # Increment the connection count
        IMAP.__add_connection()

        # Login to email with passkey
        IMAP.passkey.safe_login(self.imap.login, self.module)
        self.imap.select("inbox")


    @classmethod
    def __add_connection(cls) -> None:
        cls.connections += 1


    def __del__(self) -> None:
        # Decrement the connections counter when the instance is deleted
        IMAP.connections -= 1
