import os
from datetime import datetime

from crewai.tools import tool as crewai_tool


@crewai_tool("save_to_file")
def save_to_file(content: str, filename: str = "") -> str:
    """将内容保存到 output 目录下的 markdown 文件。

    Args:
        content: 要保存的文本内容
        filename: 文件名（不含路径），留空则自动生成
    """
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
    os.makedirs(output_dir, exist_ok=True)

    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"paper_{timestamp}.md"
    if not filename.endswith(".md"):
        filename += ".md"

    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return f"内容已保存到 {filepath}"


@crewai_tool("read_file")
def read_file(filename: str) -> str:
    """读取 output 目录下的文件内容。

    Args:
        filename: 文件名（不含路径）
    """
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
    filepath = os.path.join(output_dir, filename)

    if not os.path.exists(filepath):
        return f"文件 {filename} 不存在"

    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()
