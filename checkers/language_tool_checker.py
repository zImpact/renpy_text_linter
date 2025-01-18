import common.constants as constants
from typing import List
from common.models import Error
from utils.offset_to_row_col import offset_to_row_col
from language_tool_python import LanguageTool


class LanguageToolChecker:
    def __init__(self):
        self.tool = LanguageTool(language="ru")

    def check_text(self, text: str) -> List[Error]:
        lines = text.split("\n")
        matches = self.tool.check(text)

        errors = []
        for match in matches:
            offset = match.offset
            length = match.errorLength
            row, col = offset_to_row_col(lines, offset)

            fragment = ""
            if 0 <= row < len(lines):
                fragment = lines[row][col:col + length]

            suggestions = match.replacements if match.ruleId != "WHITESPACE_RULE" else []
            error = Error(
                checker=constants.LANGUAGE_TOOL_CHECKER,
                row=row,
                word=fragment,
                col=col,
                length=length,
                suggestions=suggestions,
                message=match.message,
            )
            errors.append(error)

        return errors
