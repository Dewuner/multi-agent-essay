from crewai import Agent, Task

from config.llm import get_llm


def create_outliner() -> Agent:
    return Agent(
        role="学术论文结构规划专家",
        goal="根据选题和文献资料，生成详细、逻辑清晰的论文大纲",
        backstory=(
            "你是一位学术论文写作指导专家，专注于帮助学者和学生规划论文结构。"
            "你擅长将复杂的研究内容组织成层次分明、逻辑连贯的论文大纲。"
            "你的大纲总是包含清晰的章节标题和每节的要点说明，让写作者可以高效地展开写作。"
        ),
        llm=get_llm(),
        verbose=True,
    )


def create_outline_task(
    agent: Agent, topic: str, course_name: str, research_notes: str
) -> Task:
    return Task(
        description=(
            f"为课程「{course_name}」的论文选题「{topic}」生成详细论文大纲。\n\n"
            "以下是文献研究阶段整理的资料：\n"
            f"{research_notes}\n\n"
            "请生成一个详细的论文大纲，包含：\n"
            "1. 论文标题（可以有 2-3 个候选）\n"
            "2. 摘要要点（100-200字）\n"
            "3. 各章节标题（至少包含引言、主体、结论三大块）\n"
            "4. 每个章节下的小节标题\n"
            "5. 每个小节的写作要点（3-5 条）\n"
            "6. 预计各章节字数分配\n"
            "7. 参考文献的引用建议\n\n"
            "目标论文总字数：3000-5000 字。\n"
            "大纲应确保逻辑连贯，各部分之间有清晰的递进关系。"
        ),
        expected_output=(
            "一份详细的论文大纲，包含标题候选、摘要要点、完整的章节结构、"
            "每节写作要点和字数分配建议。格式使用 Markdown 标题层级。"
        ),
        agent=agent,
    )
