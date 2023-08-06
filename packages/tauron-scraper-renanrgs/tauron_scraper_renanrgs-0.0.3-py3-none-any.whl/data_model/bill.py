from dataclasses import dataclass
from datetime import datetime

@dataclass
class Bill:
    amount: float
    due_date: str

    def __init__(self, amount, due_date) -> None:
        self.amount = amount
        self.due_date = due_date
