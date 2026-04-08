from crewai import Crew

from agents.outliner import create_outliner, create_outline_task


def run_outline_crew(topic: str, course_name: str, research_notes: str) -> str:
    """运行大纲规划阶段，返回论文大纲"""
    agent = create_outliner()
    task = create_outline_task(agent, topic, course_name, research_notes)

    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=True,
    )

    result = crew.kickoff()
    return str(result)
