from dataclasses import dataclass
from typing import List


@dataclass
class Error:
    code: int
    row: int
    word: str
    col: int
    length: int
    s: List[str]
