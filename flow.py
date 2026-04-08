import os
from datetime import datetime

from crews.topic_crew import run_topic_crew
from crews.research_crew import run_research_crew
from crews.outline_crew import run_outline_crew
from crews.writing_crew import run_writing_crew
from crews.review_crew import run_review_crew


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

    confirm = input("\n对大纲满意吗？(Y/n)：").strip().lower()
    if confirm == "n":
        extra = input("请输入修改建议（留空跳过）：").strip()
        if extra:
            outline = run_outline_crew(selected_topic, course_name, research_notes + "\n用户修改建议：" + extra)

    # ── Step 4: 写作 ─────────────────────────────────────────
    draft_file = _safe_filename(course_name, "draft")
    print(f"\n【阶段 4/5】撰写论文全文...\n")
    draft = run_writing_crew(
        selected_topic, course_name, outline, research_notes, draft_file
    )

    # ── Step 5: 审阅 ─────────────────────────────────────────
    final_file = _safe_filename(course_name, "final")
    print(f"\n【阶段 5/5】审阅润色...\n")
    final = run_review_crew(course_name, draft, final_file)

    # 保存最终版本
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)
    final_path = os.path.join(output_dir, final_file)
    with open(final_path, "w", encoding="utf-8") as f:
        f.write(final)

    print(f"\n{'='*60}")
    print(f"  论文写作完成！")
    print(f"  最终版本已保存到: {final_path}")
    print(f"{'='*60}\n")

    return final_path
