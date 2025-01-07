import re
import constants
from formatting_rules.base_rule import FormattingRule
from typing import List
from models import Error


class SingleQuotesRule(FormattingRule):
    def check_line(self, line: str, row_index: int) -> List[Error]:
        errors = []
        pattern = re.compile(r"'([^']+)'")

        for match in pattern.finditer(line):
            start_col = match.start()
            end_col = match.end()
            length = end_col - start_col

            inside_text = match.group(1)
            suggestion = f"«{inside_text}»"

            errors.append(Error(
                row=row_index,
                word=line[start_col:end_col],
                col=start_col,
                length=length,
                suggestions=[suggestion],
                message="Одинарные кавычки, лучше использовать «...».",
                checker=constants.FORMATTING_CHECKER
            ))

        return errors
