import argparse
import constants
from extract import extract_text, load_exclusions
from batch import create_batches
from yaspeller_checker import YaSpellerChecker
from language_tool_checker import LanguageToolChecker
from formatting_checker import FormattingChecker
from highlight import highlight_text
from typing import List


def process_file(filename: str,
                 yaspeller_checker: YaSpellerChecker,
                 language_tool_checker: LanguageToolChecker,
                 formatting_checker: FormattingChecker,
                 command_exclusions: List[str],
                 word_exclusions: List[str]):
    quoted_texts, line_positions = extract_text(filename, command_exclusions)
    batches = create_batches(quoted_texts, line_positions)

    process_file_info = f"Обработка файла: {filename}"
    process_file_info_highlighted = highlight_text(
        process_file_info, 0, len(process_file_info), "blue")
    print(process_file_info_highlighted)

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
            print(f"Батч {batch_num}: ошибок не найдено.")
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

            highlighted_line = highlight_text(
                original_text, col, length, "red")
            print(highlighted_line)

            summary = f"[{checker}]: ошибка в строке {original_line_number} - {message.lower()}"
            summary_highlighted = highlight_text(
                summary, 0, len(summary), "yellow")
            print(summary_highlighted)

            if error.suggestions:
                fixes = ", ".join(error.suggestions)
                fixes_highlighted = highlight_text(
                    fixes, 0, len(fixes), "green")
                print(f"Варианты исправления: {fixes_highlighted}")
            print()


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
    args = parser.parse_args()

    yaspeller_checker = YaSpellerChecker(api_url=constants.API_URL)
    language_tool_checker = LanguageToolChecker()
    formatting_checker = FormattingChecker()

    if args.exclusions:
        command_exclusions, word_exclusions = load_exclusions(args.exclusions)

    else:
        command_exclusions, word_exclusions = [], []

    files = args.files[0].split(" ")

    for filename in files:
        process_file(filename,
                     yaspeller_checker,
                     language_tool_checker,
                     formatting_checker,
                     command_exclusions, word_exclusions)


if __name__ == "__main__":
    main()
