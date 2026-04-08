from crewai import Crew

from agents.topic_advisor import create_topic_advisor, create_topic_task


def run_topic_crew(course_name: str, requirements: str = "") -> str:
    """运行选题阶段，返回选题建议文本"""
    agent = create_topic_advisor()
    task = create_topic_task(agent, course_name, requirements)

    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=True,
    )

    result = crew.kickoff()
    return str(result)
