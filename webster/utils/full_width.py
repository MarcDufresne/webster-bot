

def convert_normal_to_full_width(text: str) -> str:
    return "".join([chr(0xFEE0 + ord(c)) for c in text])
