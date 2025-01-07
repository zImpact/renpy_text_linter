import re
import constants
from formatting_rules.base_rule import FormattingRule
from typing import List
from models import Error


class HyphenDashRule(FormattingRule):
    def check_line(self, line: str, row_index: int) -> List[Error]:
        errors = []
        pattern = re.compile(r"\s-\s")

        for match in pattern.finditer(line):
            start_col = match.start()
            end_col = match.end()
            length = end_col - start_col
            suggestion = line.replace("-", "—")

            errors.append(Error(
                row=row_index,
                word=line[start_col:end_col],
                col=start_col,
                length=length,
                suggestions=[suggestion],
                message="Использован дефис вместо тире",
                checker=constants.FORMATTING_CHECKER
            ))

        return errors
