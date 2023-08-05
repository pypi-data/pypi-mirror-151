import os
from enum import Enum


class Environment(Enum):
    TAURON_USER = os.environ['TAURON_USER']
    TAURON_PASSWORD = os.environ['TAURON_PASSWORD']

    def __str__(self) -> str:
        return str(self.value)
