from formatting_rules.comma_no_space_after_rule import CommaNoSpaceAfterRule
from formatting_rules.double_space_rule import DoubleSpaceRule
from formatting_rules.space_at_line_start_rule import SpaceAtLineStartRule
from formatting_rules.single_quotes_rule import SingleQuotesRule
from formatting_rules.hyphen_dash_rule import HyphenDashRule
from typing import List
from models import Error


class FormattingChecker:
    def __init__(self):
        self.rules = [
            CommaNoSpaceAfterRule(),
            DoubleSpaceRule(),
            SpaceAtLineStartRule(),
            SingleQuotesRule(),
            HyphenDashRule()
        ]

    def check_text(self, text: str) -> List[Error]:
        lines = text.split("\n")
        errors = []

        for row_index, line in enumerate(lines):
            for rule in self.rules:
                rule_errors = rule.check_line(line, row_index)
                errors.extend(rule_errors)

        return errors
