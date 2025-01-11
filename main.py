import os
import argparse
import constants
from extract import extract_text, load_exclusions
from batch import create_batches
from yaspeller_checker import YaSpellerChecker
from language_tool_checker import LanguageToolChecker
from formatting_checker import FormattingChecker
from outputs.base_output import BaseOutput
from outputs.console_output import ConsoleOutput
from outputs.markdown_output import MarkdownOutput
from outputs.docx_output import DocxOutput
from outputs.txt_output import TxtOutput
from typing import List


def process_file(filename: str,
                 yaspeller_checker: YaSpellerChecker,
                 language_tool_checker: LanguageToolChecker,
                 formatting_checker: FormattingChecker,
                 outputter: BaseOutput,
                 command_exclusions: List[str],
                 word_exclusions: List[str]) -> str:
    quoted_texts, line_positions = extract_text(filename, command_exclusions)
    batches = create_batches(quoted_texts, line_positions)

    output_buffer = []
    output_buffer.append(outputter.output_header(
        f"Обработка файла: {filename}"))

    for batch_num, (batch_texts, batch_lines) in enumerate(batches, start=1):
        batch_text = "\n".join(batch_texts)

        ys_errors = yaspeller_checker.check_text(
            batch_text, lang="ru", options=0)
        lt_errors = language_tool_checker.check_text(batch_text)
        fmt_errors = formatting_checker.check_text(batch_text)

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

            summary = f"[{checker}]: ошибка в строке {original_line_number} - {message.lower()}"
            output_buffer.append(outputter.output_error(summary))

            if error.suggestions:
                fixes = ", ".join(error.suggestions)
                suggestion = f"Варианты исправления: {fixes}"
                output_buffer.append(outputter.output_suggestion(suggestion))

            output_buffer.append(outputter.output_newline())

    if type(outputter) is DocxOutput:
        return str()

    return "\n".join(output_buffer)


def main():
    parser = argparse.ArgumentParser(description="Grammar Checker Action")
    parser.add_argument(
        "files",
        metavar="FILE",
        type=str,
        nargs="+",
        help="Файлы для проверки орфографии"
    )
    parser.add_argument(
        "--exclusions",
        required=False,
        help="Исключения при проверке"
    )
    parser.add_argument(
        "--output-type",
        choices=["console", "markdown", "docx", "txt"],
        default="console"
    )
    args = parser.parse_args()

    yaspeller_checker = YaSpellerChecker(api_url=constants.YASPELLER_API_URL)
    language_tool_checker = LanguageToolChecker()
    formatting_checker = FormattingChecker()

    if args.exclusions:
        command_exclusions, word_exclusions = load_exclusions(args.exclusions)

    else:
        command_exclusions, word_exclusions = [], []

    if args.output_type == "console":
        outputter = ConsoleOutput()

    elif args.output_type == "markdown":
        outputter = MarkdownOutput()

    elif args.output_type == "docx":
        outputter = DocxOutput()

    elif args.output_type == "txt":
        outputter = TxtOutput()

    files = args.files[0].split(" ")

    all_output = []
    for filename in files:
        result = process_file(
            filename,
            yaspeller_checker,
            language_tool_checker,
            formatting_checker,
            outputter,
            command_exclusions, word_exclusions
        )
        all_output.append(result)

    if args.output_type != "docx":
        final_report = "\n".join(all_output)

    if args.output_type == "console":
        print(final_report)

    elif args.output_type == "markdown":
        summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
        if summary_file:
            with open(summary_file, "a", encoding="utf-8") as f:
                f.write(final_report + "\n")
        else:
            with open("report.md", "w", encoding="utf-8") as f:
                f.write(final_report + "\n")

    elif args.output_type == "txt":
        with open("report.txt", "w", encoding="utf-8") as f:
            f.write(final_report + "\n")

    elif args.output_type == "docx":
        outputter.save()


if __name__ == "__main__":
    main()
