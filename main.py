import argparse
import constants
from extract import extract_text, load_exclusions
from batch import create_batches
from grammar_checker import GrammarChecker
from highlight import highlight_text
from models import WordError
from typing import List


def process_file(filename: str,
                 grammar_checker: GrammarChecker,
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
        errors = grammar_checker.check_text(batch_text, lang="ru", options=0)

        if not errors:
            print(f"Батч {batch_num}: ошибок не найдено.")
            continue

        for error in errors:
            err: WordError = error

            if err.word in word_exclusions:
                continue

            if 1 <= err.row <= len(batch_texts):
                original_text = batch_texts[err.row]
                original_line = batch_lines[err.row]
                original_text_highlighted = highlight_text(
                    original_text, err.col, err.length, "red")
                print(original_text_highlighted)

                err_text = f"Ошибка в слове {err.word} на строке {original_line}."
                err_text_highlighted = highlight_text(
                    err_text, 15, err.length, "yellow")
                print(err_text_highlighted)

                if err.s:
                    fix_options = ", ".join(err.s)
                    highlighted_fixes = highlight_text(
                        fix_options, 0, len(fix_options), "green")
                    print(f"Варианты исправления: {highlighted_fixes}")
                print()

            else:
                print(f"Некорректный номер строки в ошибке: row={err.row}")


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
        required=True,
        help="Исключения при проверке"
    )
    args = parser.parse_args()

    grammar_checker = GrammarChecker(api_url=constants.API_URL)
    command_exclusions, word_exclusions = load_exclusions(args.exclusions)

    files = args.files[0].split(" ")

    for filename in files:
        process_file(filename, grammar_checker,
                     command_exclusions, word_exclusions)


if __name__ == "__main__":
    main()
