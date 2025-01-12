from outputs.base_output import BaseOutput


class InAppOutput(BaseOutput):
    def output_header(self, text: str) -> str:
        return text

    def output_info(self, text: str, col: int, length: int) -> str:
        return text

    def output_error(self, text: str) -> str:
        return text

    def output_suggestion(self, text: str) -> str:
        return text

    def output_newline(self) -> str:
        return ""
