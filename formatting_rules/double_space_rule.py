import re
import common.constants as constants
from formatting_rules.base_rule import FormattingRule
from typing import List
from common.models import Error


class DoubleSpaceRule(FormattingRule):
    def check_line(self, line: str, row_index: int) -> List[Error]:
        errors = []

        for match in re.finditer(r" {2,}", line):
            start_col = match.start()
            end_col = match.end()
            length = end_col - start_col

            errors.append(Error(
                row=row_index,
                word=line[start_col:end_col],
                col=start_col,
                length=length,
                suggestions=[],
                message="Два или более пробела подряд",
                checker=constants.FORMATTING_CHECKER
            ))

        return errors
