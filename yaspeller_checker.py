import constants
import requests
from typing import List
from models import Error


class YaSpellerChecker:
    def __init__(self, api_url: str):
        self.api_url = api_url
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

    def check_text(self,
                   text: str,
                   lang: str,
                   options: int) -> List[Error]:
        data = {
            "text": text,
            "lang": lang,
            "options": options
        }

        try:
            response = requests.post(
                self.api_url, data=data, headers=self.headers)
            response.raise_for_status()
            errors_json = response.json()
        except requests.RequestException as e:
            print(f"Ошибка при запросе к API: {e}")
            return []

        errors = [
            Error(
                checker=constants.YASPELLER_CHECKER,
                row=error.get("row", 0),
                word=error.get("word", ""),
                col=error.get("col", 0),
                length=error.get("len", 0),
                message="Орфографическая ошибка",
                suggestions=error.get("s", [])
            )
            for error in errors_json
        ]

        return errors
