import common.constants as constants


def highlight_text(line_from_file: str,
                   col: int,
                   length: int,
                   color: constants.AnsiColors) -> str:
    if col < 0 or col + length > len(line_from_file):
        return line_from_file

    before = line_from_file[:col]
    text_part = line_from_file[col:col+length]
    after = line_from_file[col+length:]

    color_code = color.value
    reset_code = constants.AnsiColors.RESET.value

    highlighted_line = f"{before}{color_code}{text_part}{reset_code}{after}"
    return highlighted_line
