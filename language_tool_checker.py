from typing import List, Tuple
from language_tool_python import LanguageTool


class LanguageToolChecker:
    def __init__(self):
        self.tool = LanguageTool(language="ru")

    def check_text(self, text):
        return self.tool.check(text)

    @staticmethod
    def offset_to_row_col(batch_lines: List[str], offset: int) -> Tuple[int, int]:
        current_offset = 0
        for row_index, line in enumerate(batch_lines):
            line_length = len(line) + 1

            if offset < current_offset + line_length:
                col_index = offset - current_offset
                return row_index, col_index

            current_offset += line_length

        return -1, -1
