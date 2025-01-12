import os
from outputs.base_output import BaseOutput


class MarkdownOutput(BaseOutput):
    def output_header(self, text: str) -> str:
        return f"<h2> 🔵 {text}</h2>"

    def output_info(self, text: str, col: int, length: int) -> str:
        before = text[:col]
        highlight = text[col:col+length]
        after = text[col+length:]

        content = "_" * \
            len(highlight) if highlight.strip() == "" else highlight
        return f"🔴 {before}<strong>{content}</strong>{after}<br />"

    def output_error(self, text: str) -> str:
        return f"🟡 <strong><em>{text}</em></strong><br />"

    def output_suggestion(self, text: str) -> str:
        fixes_len = len("Варианты исправления:")

        before = text[:fixes_len]
        suggestion_part = text[fixes_len + 1:]
        return f"🟢 {before} <strong>{suggestion_part}</strong><br />"

    def output_newline(self) -> str:
        return "<hr>"

    def save(self, final_report: str) -> None:
        summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
        if summary_file:
            with open(summary_file, "a", encoding="utf-8") as f:
                f.write(final_report + "\n")
        else:
            self.filename = "report.md"

            with open(self.filename, "w", encoding="utf-8") as f:
                f.write(final_report + "\n")
