from crewai import Agent, Task

from config.llm import get_llm
from tools.search_tool import web_search


def create_topic_advisor() -> Agent:
    return Agent(
        role="资深学术指导教授",
        goal="根据课程主题生成 3-5 个论文选题建议，每个选题包含选题理由、研究方向和预期难度",
        backstory=(
            "你是一位在高校任教多年的资深教授，擅长引导学生发现有价值的研究课题。"
            "你对文学、人文、社会科学和理工科领域都有深入了解。"
            "你的选题建议总是既有学术深度，又切合课程要求，便于学生在有限时间内完成。"
        ),
        llm=get_llm(),
        tools=[web_search],
        verbose=True,
    )


def create_topic_task(agent: Agent, course_name: str, requirements: str = "") -> Task:
    extra = f"\n额外要求：{requirements}" if requirements else ""
    return Task(
        description=(
            f"为课程「{course_name}」生成 3-5 个课程论文选题建议。{extra}\n\n"
            "请为每个选题提供：\n"
            "1. 选题标题\n"
            "2. 选题理由（为什么这个选题有价值）\n"
            "3. 研究方向（可以从哪些角度展开）\n"
            "4. 预期难度（简单/中等/较难）\n"
            "5. 推荐参考资料关键词\n\n"
            "请先用搜索工具了解该课程领域的热门研究方向，再生成选题。"
        ),
        expected_output=(
            "一份包含 3-5 个选题建议的列表，每个选题包含标题、理由、研究方向、难度和参考关键词。"
            "格式清晰，方便用户选择。"
        ),
        agent=agent,
    )
