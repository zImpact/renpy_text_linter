from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout,
    QWidget, QFileDialog, QComboBox, QTextEdit
)
from outputs.in_app_output import InAppOutput
from outputs.markdown_output import MarkdownOutput
from outputs.docx_output import DocxOutput
from outputs.txt_output import TxtOutput
from checkers.yaspeller_checker import YaSpellerChecker
from checkers.language_tool_checker import LanguageToolChecker
from checkers.formatting_checker import FormattingChecker
from utils.process import process_file
import common.constants as constants
import sys


class RenpyTextLinterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("RenpyTextLinter")
        self.setGeometry(100, 100, 800, 600)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        layout = QVBoxLayout()

        self.label = QLabel("Выберите файл для проверки текста")
        layout.addWidget(self.label)

        self.file_button = QPushButton("Выбрать файл")
        self.file_button.clicked.connect(self.select_file)
        layout.addWidget(self.file_button)

        self.output_type_combobox = QComboBox()
        self.output_type_combobox.addItems(
            [output_type.value for output_type in constants.APP_OUTPUT_FORMATS]
        )
        layout.addWidget(self.output_type_combobox)

        self.run_button = QPushButton("Запустить проверку")
        self.run_button.clicked.connect(self.run_grammar_check)
        layout.addWidget(self.run_button)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)

        self.centralWidget.setLayout(layout)

    def select_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self, "Выберите файл", "", "All Files (*)"
        )
        if file_path:
            self.file_path = file_path
            self.label.setText(f"Выбран файл: {file_path}")

    def run_grammar_check(self):
        if not hasattr(self, "file_path") or not self.file_path:
            self.result_text.setHtml("Выберите файл для проверки")
            return

        output_type = self.output_type_combobox.currentText()
        outputter = {
            constants.OutputType.IN_APP.value: InAppOutput(),
            constants.OutputType.MARKDOWN.value: MarkdownOutput(),
            constants.OutputType.DOCX.value: DocxOutput(),
            constants.OutputType.TXT.value: TxtOutput()
        }.get(output_type, InAppOutput())

        # TODO: добавить возможность подгрузки исключений для десктоп-версии
        command_exclusions, word_exclusions = [], []

        try:
            yaspeller_checker = YaSpellerChecker(
                api_url=constants.YASPELLER_API_URL)
            language_tool_checker = LanguageToolChecker()
            formatting_checker = FormattingChecker()

            result = process_file(
                self.file_path,
                yaspeller_checker,
                language_tool_checker,
                formatting_checker,
                outputter,
                command_exclusions, word_exclusions
            )

            if output_type == constants.OutputType.IN_APP.value:
                self.result_text.setHtml(result)
            else:
                if output_type == constants.OutputType.DOCX.value:
                    outputter.save()
                else:
                    outputter.save(result)

                self.result_text.setText(
                    f"Результат сохранён в файле: {outputter.filename}")

        except Exception as e:
            self.result_text.setHtml(f"Произошла ошибка: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RenpyTextLinterApp()
    window.show()
    sys.exit(app.exec())
