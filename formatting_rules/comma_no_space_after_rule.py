import re
import common.constants as constants
from formatting_rules.base_rule import FormattingRule
from typing import List
from common.models import Error


class CommaNoSpaceAfterRule(FormattingRule):
    def check_line(self, line: str, row_index: int) -> List[Error]:
        errors = []
        pattern = re.compile(r",(?!\s)")

        for match in pattern.finditer(line):
            start_col = match.start()
            errors.append(Error(
                row=row_index,
                word=",",
                col=start_col,
                length=1,
                suggestions=[],
                message="Нет пробела после запятой",
                checker=constants.FORMATTING_CHECKER
            ))

        return errors
