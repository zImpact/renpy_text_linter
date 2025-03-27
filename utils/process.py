from checkers.yaspeller_checker import YaSpellerChecker
from checkers.language_tool_checker import LanguageToolChecker
from checkers.formatting_checker import FormattingChecker
from outputs.base_output import BaseOutput
from outputs.docx_output import DocxOutput
from utils.batch import create_batches
from utils.extract import extract_text
from typing import List


def process_file(filename: str,
                 yaspeller_checker: YaSpellerChecker,
                 language_tool_checker: LanguageToolChecker,
                 formatting_checker: FormattingChecker,
                 outputter: BaseOutput,
                 word_exclusions: List[str]) -> str:
    quoted_texts, line_positions = extract_text(filename)
    batches = create_batches(quoted_texts, line_positions)

    output_buffer = []
    output_buffer.append(outputter.output_header(
        f"Обработка файла: {filename}"))

    for batch_num, (batch_texts, batch_lines) in enumerate(batches, start=1):
        batch_text = "\n".join(batch_texts)

        ys_errors = yaspeller_checker.check_text(
            batch_text,
            lang="ru",
            options=0
        )
        lt_errors = language_tool_checker.check_text(
            batch_text
        )
        fmt_errors = formatting_checker.check_text(
            batch_text
        )

        if word_exclusions:
            ys_errors = [e for e in ys_errors if e.word not in word_exclusions]
            lt_errors = [e for e in lt_errors if e.word not in word_exclusions]

        combined_errors = ys_errors + lt_errors + fmt_errors

        if not combined_errors:
            output_buffer.append(outputter.output_header(
                f"Батч {batch_num}: ошибок не найдено."))
            continue

        combined_errors.sort(key=lambda e: (e.row, e.col))

        for error in combined_errors:
            row = error.row
            col = error.col
            length = error.length
            message = error.message
            checker = error.checker

            original_text = batch_texts[row]
            original_line_number = batch_lines[row]

            output_buffer.append(outputter.output_info(
                original_text, col, length))

            summary = (
                f"[{checker}]: ошибка в строке {original_line_number} — "
                f"{message.lower()}"
            )

            output_buffer.append(outputter.output_error(summary))

            if error.suggestions:
                suggestion = ", ".join(error.suggestions)
                output_buffer.append(outputter.output_suggestion(suggestion))

            output_buffer.append(outputter.output_newline())

    if type(outputter) is DocxOutput:
        return str()

    return "\n".join(output_buffer)
