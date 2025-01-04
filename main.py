import argparse
import constants
from extract import extract_text, load_exclusions
from batch import create_batches
from yaspeller_checker import YaSpellerChecker
from language_tool_checker import LanguageToolChecker
from highlight import highlight_text
from typing import Any, Dict, List


def process_file(filename: str,
                 yaspeller_checker: YaSpellerChecker,
                 language_tool_checker: LanguageToolChecker,
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

        if not ys_errors and not lt_errors:
            print(f"Батч {batch_num}: ошибок не найдено.")
            continue

        combined_errors: List[Dict[str, Any]] = []

        for ys_error in ys_errors:
            if ys_error.word in word_exclusions:
                continue

            combined_errors.append({
                "checker": "YaSpeller",
                "row": ys_error.row,
                "col": ys_error.col,
                "length": ys_error.length,
                "text": ys_error.word,
                "message": "Орфографическая ошибка",
                "suggestions": ys_error.s
            })

        for lt_error in lt_errors:
            offset = lt_error.offset
            length = lt_error.errorLength
            row, col = language_tool_checker.offset_to_row_col(
                batch_texts, offset)

            fragment = batch_texts[row][col: col + length]
            if fragment in word_exclusions:
                continue

            combined_errors.append({
                "checker": "LanguageTool",
                "row": row,
                "col": col,
                "length": length,
                "text": fragment,
                "message": lt_error.message,
                "suggestions": lt_error.replacements
            })

        combined_errors.sort(key=lambda e: (e["row"], e["col"]))

        for error in combined_errors:
            row = error["row"]
            col = error["col"]
            length = error["length"]
            message = error["message"]
            checker = error["checker"]

            original_text = batch_texts[row]
            original_line_number = batch_lines[row]

            highlighted_line = highlight_text(
                original_text, col, length, "red")
            print(highlighted_line)

            summary = f"[{checker}]: ошибка в строке {original_line_number} - {message.lower()}"
            summary_highlighted = highlight_text(
                summary, 0, len(summary), "yellow")
            print(summary_highlighted)

            if error["suggestions"]:
                fixes = ", ".join(error["suggestions"])
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

    if args.exclusions:
        command_exclusions, word_exclusions = load_exclusions(args.exclusions)

    else:
        command_exclusions, word_exclusions = [], []

    files = args.files[0].split(" ")

    for filename in files:
        process_file(filename, yaspeller_checker, language_tool_checker,
                     command_exclusions, word_exclusions)


if __name__ == "__main__":
    main()
