from crewai import Crew

from agents.reviewer import create_reviewer, create_review_task


def run_review_crew(course_name: str, draft_content: str) -> str:
    """运行审阅润色阶段，返回最终论文全文"""
    agent = create_reviewer()
    task = create_review_task(agent, course_name, draft_content)

    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=True,
    )

    result = crew.kickoff()
    return str(result)
