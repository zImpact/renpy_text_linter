import re
import yaml
from typing import List, Tuple


def load_exclusions(exclusions_file_path: str) -> List[str]:
    with open(exclusions_file_path, "r", encoding="utf-8") as f:
        exclusions = yaml.safe_load(f)

    return exclusions.get("words", [])


def extract_text(filename: str) -> Tuple[List[str], List[int]]:
    quoted_texts = []
    line_positions = []

    pattern = re.compile(r'"((?:\\.|[^"\\])*)"')
    text_pattern = re.compile(r'\{[^}]+\}')

    with open(filename, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue

            if line.endswith("nolint"):
                continue

            matches = pattern.findall(line)
            for match in matches:
                text = text_pattern.sub("", match).replace("\\n", " ").strip()

                if re.search(r"[А-Яа-яЁё]", text):
                    quoted_texts.append(text)
                    line_positions.append(i)

    return quoted_texts, line_positions
