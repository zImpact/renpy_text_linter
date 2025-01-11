import constants
from typing import List, Tuple
from models import Error
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
            row, col = self.offset_to_row_col(lines, offset)

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

    @staticmethod
    def offset_to_row_col(lines: List[str], offset: int) -> Tuple[int, int]:
        current_offset = 0
        for row_index, line in enumerate(lines):
            line_length = len(line) + 1

            if offset < current_offset + line_length:
                col_index = offset - current_offset
                return row_index, col_index

            current_offset += line_length

        return -1, -1
