from crewai import Crew

from agents.writer import create_writer, create_writing_task


def run_writing_crew(
    topic: str,
    course_name: str,
    outline: str,
    research_notes: str,
    filename: str,
) -> str:
    """运行论文写作阶段，返回论文草稿"""
    agent = create_writer()
    task = create_writing_task(agent, topic, course_name, outline, research_notes, filename)

    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=True,
    )

    result = crew.kickoff()
    return str(result)
