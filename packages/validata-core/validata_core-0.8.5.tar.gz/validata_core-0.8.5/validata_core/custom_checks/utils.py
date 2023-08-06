from frictionless import errors


def build_check_error(custom_check_code: str, note: str):
    custom_note = f"{custom_check_code!r}: {note}"
    return errors.CheckError(note=custom_note)
