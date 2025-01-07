from dataclasses import dataclass
from typing import List


@dataclass
class Error:
    checker: str
    row: int
    word: str
    col: int
    length: int
    message: str
    suggestions: List[str]
