import os
import argparse
import pathlib
import common.constants as constants
from utils.process import process_file
from utils.extract import load_exclusions
from checkers.yaspeller_checker import YaSpellerChecker
from checkers.language_tool_checker import LanguageToolChecker
from checkers.formatting_checker import FormattingChecker
from outputs.console_output import ConsoleOutput
from outputs.markdown_output import MarkdownOutput
from outputs.docx_output import DocxOutput
from outputs.txt_output import TxtOutput


def main():
    parser = argparse.ArgumentParser(description="Renpy Text Linter")
    parser.add_argument(
        "paths",
        metavar="PATH",
        type=str,
        nargs=1,
        help="Файлы или директории для проверки орфографии"
    )
    parser.add_argument(
        "--exclusions",
        required=False,
        help="Исключения при проверке"
    )
    parser.add_argument(
        "--output-type",
        choices=[output.value for output in constants.CONSOLE_OUTPUT_FORMATS],
        default=constants.OutputType.CONSOLE.value
    )
    args = parser.parse_args()

    yaspeller_checker = YaSpellerChecker(api_url=constants.YASPELLER_API_URL)
    language_tool_checker = LanguageToolChecker()
    formatting_checker = FormattingChecker()

    word_exclusions = load_exclusions(
        args.exclusions) if args.exclusions else []

    outputter = {
        constants.OutputType.CONSOLE.value: ConsoleOutput(),
        constants.OutputType.MARKDOWN.value: MarkdownOutput(),
        constants.OutputType.DOCX.value: DocxOutput(),
        constants.OutputType.TXT.value: TxtOutput()
    }.get(args.output_type, ConsoleOutput())

    files = []
    for path in args.paths[0].split():
        p = pathlib.Path(path)
        if p.is_dir():
            for file in p.rglob("*.rpy"):
                files.append(str(file))

        else:
            files.append(str(p))

    all_output = []
    for filename in files:
        result = process_file(
            filename,
            yaspeller_checker,
            language_tool_checker,
            formatting_checker,
            outputter,
            word_exclusions
        )
        all_output.append(result)

    if args.output_type != constants.OutputType.DOCX.value:
        final_report = "\n".join(all_output)

    if args.output_type == constants.OutputType.CONSOLE.value:
        print(final_report)

    else:
        if args.output_type == constants.OutputType.DOCX.value:
            outputter.save()
        else:
            outputter.save(final_report)

        if not os.environ.get("GITHUB_STEP_SUMMARY"):
            print(f"Результат сохранён в файле: {outputter.filename}")


if __name__ == "__main__":
    main()
