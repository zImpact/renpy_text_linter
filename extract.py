import re
import yaml
from typing import List, Tuple


def load_exclusions(exclusions_file_path: str) -> Tuple[List[str], List[str]]:
    with open(exclusions_file_path, "r", encoding="utf-8") as f:
        exclusions = yaml.safe_load(f)

    commands = exclusions.get("commands", [])
    words = exclusions.get("words", [])
    return commands, words


def extract_text(filename: str,
                 command_exclusions: List[str]) -> Tuple[List[str], List[int]]:
    quoted_texts = []
    line_positions = []
    pattern = re.compile(r'"([^"]+)"')

    with open(filename, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue

            if any(line.startswith(command) for command in command_exclusions):
                continue

            matches = pattern.findall(line)
            for match in matches:
                quoted_texts.append(match)
                line_positions.append(i)

    return quoted_texts, line_positions
