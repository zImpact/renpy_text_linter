import common.constants as constants
from outputs.base_output import BaseOutput
from utils.highlight import highlight_text


class ConsoleOutput(BaseOutput):
    def output_header(self, text: str) -> str:
        return highlight_text(text, 0, len(text), constants.AnsiColors.BLUE)

    def output_info(self, text: str, col: int, length: int) -> str:
        return highlight_text(text, col, length, constants.AnsiColors.RED)

    def output_error(self, text: str) -> str:
        return highlight_text(text, 0, len(text), constants.AnsiColors.YELLOW)

    def output_suggestion(self, text: str) -> str:
        fixes = highlight_text(text, 0, len(text), constants.AnsiColors.GREEN)
        return f"Варианты исправления: {fixes}"

    def output_newline(self) -> str:
        return str()
