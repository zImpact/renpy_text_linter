from outputs.base_output import BaseOutput


class TxtOutput(BaseOutput):
    def output_header(self, text: str) -> str:
        return f"{'+' * 40}\n{text}\n{'+' * 40}\n"

    def output_info(self, text: str, col: int, length: int) -> str:
        before = text[:col]
        highlight = text[col:col+length]
        after = text[col+length:]

        content = "_" * \
            len(highlight) if highlight.strip() == "" else highlight

        return f"{before}<{content}>{after}"

    def output_error(self, text: str) -> str:
        return f"{text}"

    def output_suggestion(self, text: str) -> str:
        return f"Варианты исправления: <{text}>"

    def output_newline(self) -> str:
        return f"\n{'=' * 40}\n"

    def save(self, final_report: str) -> None:
        self.filename = "report.txt"

        with open(self.filename, "w", encoding="utf-8") as f:
            f.write(final_report + "\n")
