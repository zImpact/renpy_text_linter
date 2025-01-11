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
        fixes_len = len("Варианты исправления:")

        before = text[:fixes_len]
        suggestion_part = text[fixes_len + 1:]
        return f"{before} <{suggestion_part}>"

    def output_newline(self) -> str:
        return f"\n{'=' * 40}\n"
