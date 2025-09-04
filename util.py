import os


def load_hotel_introduction(file_path="hotel_introd.txt"):
    current_dir = os.path.dirname(__file__)
    full_path = os.path.join(current_dir, file_path)

    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    return content
