import os
import sys
import termios
from datetime import datetime

from crews.topic_crew import run_topic_crew
from crews.research_crew import run_research_crew
from crews.outline_crew import run_outline_crew
from crews.writing_crew import run_writing_crew
from crews.review_crew import run_review_crew


def _clear_stdin():
    """清空 stdin 缓冲区，防止 CrewAI 输出残留被 input() 误读"""
    try:
        termios.tcflush(sys.stdin, termios.TCIFLUSH)
    except Exception:
        pass


def _safe_filename(course_name: str, suffix: str) -> str:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe = course_name.replace(" ", "_")
    return f"{safe}_{suffix}_{ts}.md"


def run_full_flow(course_name: str, requirements: str = "") -> str:
    """运行完整的论文写作流程，返回最终论文文件路径。

    在选题和大纲阶段会暂停等待用户确认。
    """
    print(f"\n{'='*60}")
    print(f"  课程论文写作系统 — {course_name}")
    print(f"{'='*60}\n")

    # ── Step 1: 选题 ──────────────────────────────────────────
    print("【阶段 1/5】生成选题建议...\n")
    topic_suggestions = run_topic_crew(course_name, requirements)

    print("\n" + "=" * 60)
    print("选题建议如下：")
    print("=" * 60)
    print(topic_suggestions)

    _clear_stdin()
    selected_topic = input(
        "\n请输入你选择的选题（可以照抄标题，也可以自行输入）：\n> "
    ).strip()
    if not selected_topic:
        selected_topic = "（使用默认选题）"

    # ── Step 2: 文献研究 ─────────────────────────────────────
    print(f"\n【阶段 2/5】搜索「{selected_topic}」相关文献...\n")
    research_notes = run_research_crew(selected_topic, course_name)

    # ── Step 3: 大纲 ─────────────────────────────────────────
    print("\n【阶段 3/5】生成论文大纲...\n")
    outline = run_outline_crew(selected_topic, course_name, research_notes)

    print("\n" + "=" * 60)
    print("论文大纲如下：")
    print("=" * 60)
    print(outline)

    _clear_stdin()
    confirm = input("\n对大纲满意吗？(Y/n)：").strip().lower()
    if confirm == "n":
        _clear_stdin()
        extra = input("请输入修改建议（留空跳过）：").strip()
        if extra:
            outline = run_outline_crew(selected_topic, course_name, research_notes + "\n用户修改建议：" + extra)

    # ── Step 4: 写作 ─────────────────────────────────────────
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)

    draft_file = _safe_filename(course_name, "draft")
    print(f"\n【阶段 4/5】撰写论文全文...\n")
    run_writing_crew(
        selected_topic, course_name, outline, research_notes, draft_file
    )

    # 从保存的文件读取实际论文内容（crew 返回的是摘要，不是论文）
    draft_path = os.path.join(output_dir, draft_file)
    with open(draft_path, "r", encoding="utf-8") as f:
        draft = f.read()

    # ── Step 5: 审阅 ─────────────────────────────────────────
    final_file = _safe_filename(course_name, "final")
    print(f"\n【阶段 5/5】审阅润色...\n")
    run_review_crew(course_name, draft, final_file)

    # 审阅后的最终版本已由 reviewer 保存到文件，直接读取
    final_path = os.path.join(output_dir, final_file)
    # 如果 reviewer 返回的是摘要而非论文内容，需要从保存的文件读取
    if not os.path.exists(final_path) or os.path.getsize(final_path) < 100:
        # 文件不存在或太小，说明 reviewer 没有正确保存，使用 draft 作为最终版
        final_path = draft_path

    print(f"\n{'='*60}")
    print(f"  论文写作完成！")
    print(f"  最终版本已保存到: {final_path}")
    print(f"{'='*60}\n")

    return final_path
