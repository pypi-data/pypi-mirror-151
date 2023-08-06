import os
from abc import ABC
from dataclasses import dataclass
from enum import Enum


class Credentials(Enum):
    GMAIL_USER = os.environ['EMAIL']
    GMAIL_PASSWORD = os.environ['GMAIL_PASSWORD_APP']


@dataclass(frozen=True, init=False)
class EmailCredentials(ABC):
    user: str
    password: str


@dataclass(frozen=True, init=False)
class GmailCredentials(EmailCredentials):
    user: str = Credentials.GMAIL_USER.value
    password: str = Credentials.GMAIL_PASSWORD.value

