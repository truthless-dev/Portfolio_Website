import louis


def braille_to_print(table_list: list[str], input: str = "") -> list[str] | None:
    input_lines = input.split("\n")
    try:
        return [
            louis.backTranslateString(table_list, input_line)
            for input_line in input_lines
        ]
    except Exception:
        return None
