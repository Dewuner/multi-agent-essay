from crewai import Agent, Task

from config.llm import get_llm


def create_reviewer() -> Agent:
    return Agent(
        role="严格但公正的学术审稿人",
        goal="审阅论文，检查逻辑、结构、语言质量，进行润色修改，输出最终版本",
        backstory=(
            "你是一位严谨的学术期刊审稿人，同时也是一位出色的学术写作编辑。"
            "你在审阅论文时既关注学术内容的严谨性，也关注写作的规范性。"
            "你不仅指出问题，还会直接给出修改后的文本。"
            "你的审阅意见总是建设性的，帮助作者提升论文质量。"
        ),
        llm=get_llm(),
        verbose=True,
    )


def create_review_task(
    agent: Agent,
    course_name: str,
    draft_content: str,
) -> Task:
    return Task(
        description=(
            f"审阅并润色课程「{course_name}」的论文草稿。\n\n"
            "以下是论文草稿：\n"
            f"{draft_content}\n\n"
            "请完成以下审阅工作：\n"
            "1. 检查论文结构是否完整、逻辑是否连贯\n"
            "2. 检查论点是否清晰、论据是否充分\n"
            "3. 检查语言表达是否准确、流畅、学术化\n"
            "4. 检查格式是否规范（标题层级、引用格式等）\n"
            "5. 对发现的问题直接进行润色修改\n"
            "6. 确保总字数在 3000-5000 字范围内\n\n"
            "重要：你的最终回复必须是润色后的完整论文全文（Markdown 格式），"
            "不要只给出审阅意见或摘要。在论文末尾附上简短的审阅说明。"
        ),
        expected_output=(
            "经过审阅和润色后的完整论文全文（Markdown 格式），"
            "论文末尾附有审阅说明。字数 3000-5000 字。"
        ),
        agent=agent,
    )
