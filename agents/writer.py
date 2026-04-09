from crewai import Agent, Task

from config.llm import get_llm


def create_writer() -> Agent:
    return Agent(
        role="学术论文写作专家",
        goal="按照大纲和文献资料，撰写高质量的课程论文全文",
        backstory=(
            "你是一位专业的学术论文写作者，拥有丰富的学术写作经验。"
            "你擅长将研究资料和大纲转化为流畅、严谨的学术论文。"
            "你的写作风格既保持学术规范性，又不失可读性。"
            "你特别注意论点的逻辑性、论据的充分性和语言的准确性。"
        ),
        llm=get_llm(),
        verbose=True,
    )


def create_writing_task(
    agent: Agent,
    topic: str,
    course_name: str,
    outline: str,
    research_notes: str,
) -> Task:
    return Task(
        description=(
            f"为课程「{course_name}」撰写论文「{topic}」的全文。\n\n"
            "以下是论文大纲：\n"
            f"{outline}\n\n"
            "以下是文献研究资料：\n"
            f"{research_notes}\n\n"
            "请按照大纲结构，逐章节撰写完整的论文。要求：\n"
            "1. 严格遵循大纲结构\n"
            "2. 每个章节都要充分展开，论点清晰，论据充分\n"
            "3. 适当引用文献研究中的观点和数据\n"
            "4. 语言学术规范，逻辑清晰\n"
            "5. 总字数控制在 3000-5000 字\n"
            "6. 包含参考文献列表\n"
            "7. 使用 Markdown 格式\n\n"
            "重要：你的最终回复必须是完整的论文全文（Markdown 格式），"
            "不要只给出摘要或说明。直接输出论文内容，不要添加任何前言或总结。"
        ),
        expected_output=(
            "完整的课程论文全文（Markdown 格式），包含标题、摘要、正文各章节和参考文献。"
            "字数 3000-5000 字。"
        ),
        agent=agent,
    )
