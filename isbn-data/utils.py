import unicodedata
import logging


log = logging.getLogger(__name__)

COMBINING_MAP = {
    "COMBINING ACUTE ACCENT": "WITH ACUTE",
    "COMBINING OGONEK": "WITH OGONEK",
    "COMBINING LONG SOLIDUS OVERLAY": "WITH STROKE",
    "COMBINING DOT ABOVE": "WITH DOT ABOVE",
    "COMBINING LEFT HALF RING BELOW": "WITH ACUTE",  # technically, this is wrong
    "COMBINING DIAERESIS": "WITH DIAERESIS",
    "COMBINING CARON": "WITH CARON",
}

def sanitize_string(string):
    if string is None:
        return ""

    output_string = []

    for idx, char in enumerate(string):
        output_string.append(char)
        if (
            (combining_name := unicodedata.name(char))
            and combining_name.startswith("COMBINING")
        ):
            combined_char = output_string.pop()
            base_char = output_string.pop()
            suffix = COMBINING_MAP.get(combining_name)
            if not suffix:
                log.critical(
                    "Got unknown combining char '%s' ('%s') in string '%s'",
                    combining_name, combined_char, string
                )
            base_char_name = unicodedata.name(base_char)
            combined_char_name = f"{base_char_name} {suffix}"
            combined_char = unicodedata.lookup(combined_char_name)
            output_string.append(combined_char)

    return "".join(output_string)
