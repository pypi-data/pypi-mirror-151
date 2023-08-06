from dataclasses import asdict, dataclass

from config.env_enum import Environment
from util.singleton import singleton


@singleton
@dataclass(frozen=True)
class UserData:
    username: str = Environment.TAURON_USER.value
    password: str = Environment.TAURON_PASSWORD.value
