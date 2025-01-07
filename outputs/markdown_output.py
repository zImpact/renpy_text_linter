from outputs.base_output import BaseOutput


class MarkdownOutput(BaseOutput):
    def output_header(self, text: str) -> str:
        return f"## 🔵 {text}<br />"

    def output_info(self, text: str, col: int, length: int) -> str:
        before = text[:col]
        highlight = text[col:col+length]
        after = text[col+length:]

        return f"🔴 {before}**~~{highlight}~~**{after}<br />"

    def output_error(self, text: str) -> str:
        return f"🟡 ***{text}***<br />"

    def output_suggestion(self, text: str) -> str:
        fixes_len = len("Варианты исправления:")

        before = text[:fixes_len]
        suggestion_part = text[fixes_len:]
        return f"🟢 {before}**{suggestion_part}**<br />"
