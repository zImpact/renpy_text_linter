from typing import List, Tuple


def offset_to_row_col(lines: List[str], offset: int) -> Tuple[int, int]:
    current_offset = 0
    for row_index, line in enumerate(lines):
        line_length = len(line) + 1

        if offset < current_offset + line_length:
            col_index = offset - current_offset
            return row_index, col_index

        current_offset += line_length

    return -1, -1
