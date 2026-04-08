from crewai import Agent, Task

from config.llm import get_llm
from tools.search_tool import web_search


def create_researcher() -> Agent:
    return Agent(
        role="学术文献研究专家",
        goal="针对选定主题搜索和整理相关文献，提取关键观点，建立参考文献列表",
        backstory=(
            "你是一位经验丰富的学术文献研究员，擅长使用各类学术搜索引擎和数据库。"
            "你能快速定位相关文献，提取核心观点，并整理成结构化的研究笔记。"
            "你的文献综述总能帮助写作者快速把握研究领域的全貌。"
        ),
        llm=get_llm(),
        tools=[web_search],
        verbose=True,
    )


def create_research_task(agent: Agent, topic: str, course_name: str) -> Task:
    return Task(
        description=(
            f"为课程「{course_name}」的论文选题「{topic}」搜索和整理相关文献资料。\n\n"
            "请完成以下工作：\n"
            "1. 使用搜索工具搜索与选题相关的学术资料、新闻、案例分析\n"
            "2. 整理出 8-15 条关键观点或研究发现\n"
            "3. 对关键观点进行分类（如理论支持、案例分析、数据统计等）\n"
            "4. 整理参考文献列表（包含标题、来源、关键内容摘要）\n"
            "5. 指出当前研究中的空白或有争议的地方\n\n"
            "搜索建议：使用多个不同角度的关键词进行搜索，确保覆盖面广泛。"
        ),
        expected_output=(
            "一份结构化的文献研究报告，包含：\n"
            "- 关键观点分类整理\n"
            "- 参考文献列表（含摘要）\n"
            "- 研究空白和分析\n"
            "- 对论文写作的建议"
        ),
        agent=agent,
    )
