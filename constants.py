from enum import Enum


class AnsiColors(Enum):
    RED = "\x1b[31m"
    GREEN = "\x1b[32m"
    YELLOW = "\x1b[33m"
    BLUE = "\x1b[34m"


class OutputType(Enum):
    CONSOLE = "console"
    IN_APP = "in app"
    MARKDOWN = "markdown"
    DOCX = "docx"
    TXT = "txt"


YASPELLER_API_URL = "https://speller.yandex.net/services/spellservice.json/checkText"

YASPELLER_CHECKER = "YaSpeller"
LANGUAGE_TOOL_CHECKER = "LanguageTool"
FORMATTING_CHECKER = "Formatting"

WORD_TIMES_NEW_ROMAN_FONT = "Times New Roman"
WORD_HEADER_SIZE = 14
WORD_MAIN_TEXT_SIZE = 12

CONSOLE_OUTPUT_FORMATS = [
    OutputType.CONSOLE,
    OutputType.MARKDOWN,
    OutputType.DOCX,
    OutputType.TXT
]

APP_OUTPUT_FORMATS = [
    OutputType.IN_APP,
    OutputType.MARKDOWN,
    OutputType.DOCX,
    OutputType.TXT
]
