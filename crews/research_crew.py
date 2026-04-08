from crewai import Crew

from agents.researcher import create_researcher, create_research_task


def run_research_crew(topic: str, course_name: str) -> str:
    """运行文献研究阶段，返回研究笔记"""
    agent = create_researcher()
    task = create_research_task(agent, topic, course_name)

    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=True,
    )

    result = crew.kickoff()
    return str(result)
