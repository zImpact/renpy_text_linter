import argparse
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
        choices=[output.value for output in constants.CONSOLE_OUTPUT_FORMATS],
        default=constants.OutputType.CONSOLE.value
    )
    args = parser.parse_args()

    yaspeller_checker = YaSpellerChecker(api_url=constants.YASPELLER_API_URL)
    language_tool_checker = LanguageToolChecker()
    formatting_checker = FormattingChecker()

    if args.exclusions:
        command_exclusions, word_exclusions = load_exclusions(args.exclusions)

    else:
        command_exclusions, word_exclusions = [], []

    outputter = {
        constants.OutputType.CONSOLE.value: ConsoleOutput(),
        constants.OutputType.MARKDOWN.value: MarkdownOutput(),
        constants.OutputType.DOCX.value: DocxOutput(),
        constants.OutputType.TXT.value: TxtOutput()
    }.get(args.output_type, ConsoleOutput())

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

    if args.output_type != constants.OutputType.DOCX.value:
        final_report = "\n".join(all_output)

    if args.output_type == constants.OutputType.CONSOLE.value:
        print(final_report)

    else:
        if args.output_type == constants.OutputType.DOCX.value:
            outputter.save()
        else:
            outputter.save(final_report)

        print(f"Результат сохранён в файле: {outputter.filename}")


if __name__ == "__main__":
    main()
