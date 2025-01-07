from typing import Protocol


class BaseOutput(Protocol):
    def output_header(self, text: str) -> str:
        raise NotImplementedError

    def output_info(self, text: str) -> str:
        raise NotImplementedError

    def output_error(self, text: str) -> str:
        raise NotImplementedError

    def output_suggestion(self, text: str) -> str:
        raise NotImplementedError
