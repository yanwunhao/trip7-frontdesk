import os


def load_hotel_introduction(file_path="hotel_introd.txt"):
    current_dir = os.path.dirname(__file__)
    full_path = os.path.join(current_dir, file_path)

    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    return content


def jobinfo2markdown(jobinfo: dict) -> str:
    """
    Convert job information JSON to Markdown format

    Args:
        jobinfo: Dictionary containing departments list with positions

    Returns:
        Formatted Markdown string
    """
    markdown_lines = ["# 招聘職位一覧\n"]

    departments = jobinfo.get('departments', [])

    for dept in departments:
        dept_name = dept.get('name', '')
        positions = dept.get('positions', [])

        # Department heading
        markdown_lines.append(f"## {dept_name}\n")

        # Iterate through all positions in this department
        for position in positions:
            title = position.get('title', '')
            salary = position.get('salary', '')
            description = position.get('description', '')

            # Position details
            markdown_lines.append(f"### {title}\n")
            markdown_lines.append(f"**給与範囲:** {salary}\n")
            markdown_lines.append(f"**職務内容:** {description}\n")
            markdown_lines.append("")  # Empty line separator

    return "\n".join(markdown_lines)
