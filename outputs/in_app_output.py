from outputs.base_output import BaseOutput


class InAppOutput(BaseOutput):
    def output_header(self, text: str) -> str:
        return f"<h2 style='color: blue;'>{text}</h2>"

    def output_info(self, text: str, col: int, length: int) -> str:
        before = text[:col]
        highlight = text[col:col+length]
        after = text[col+length:]
        return f"<p style='color: green;'>{before}<span style='color: red;'>{highlight}</span>{after}</p>"

    def output_error(self, text: str) -> str:
        return f"<p style='yellow: red;'><b>Ошибка:</b> {text}</p>"

    def output_suggestion(self, text: str) -> str:
        return f"<p>Варианты исправления: <span style='color: orange;'>{text}</span></p>"

    def output_newline(self) -> str:
        return "<br>"
