from outputs.base_output import BaseOutput
from highlight import highlight_text


class ConsoleOutput(BaseOutput):
    def output_header(self, text: str) -> str:
        return highlight_text(text, 0, len(text), "blue")

    def output_info(self, text: str, col: int, length: int) -> str:
        return highlight_text(text, col, length, "red")

    def output_error(self, text: str) -> str:
        return highlight_text(text, 0, len(text), "yellow")

    def output_suggestion(self, text: str) -> str:
        fixes_len = len("Варианты исправления:")
        return highlight_text(text, fixes_len, len(text) - fixes_len, "green")
