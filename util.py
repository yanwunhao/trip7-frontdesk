import os


def load_hotel_introduction(file_path="hotel_introd.txt"):
    current_dir = os.path.dirname(__file__)
    full_path = os.path.join(current_dir, file_path)

    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    return content


def additionalinfo2markdown(data: dict) -> str:
    """
    Convert additional information dictionary to Markdown format

    Args:
        data: Dictionary containing any structured data

    Returns:
        Formatted Markdown string
    """
    def process_value(value, level=1):
        lines = []
        if isinstance(value, dict):
            for key, val in value.items():
                lines.append(f"{'#' * level} {key}\n")
                lines.extend(process_value(val, level + 1))
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    lines.extend(process_value(item, level))
                else:
                    lines.append(f"- {item}\n")
        else:
            lines.append(f"{value}\n")
        return lines

    markdown_lines = []
    for key, value in data.items():
        markdown_lines.append(f"# {key}\n")
        markdown_lines.extend(process_value(value, 2))
        markdown_lines.append("")

    return "\n".join(markdown_lines)
