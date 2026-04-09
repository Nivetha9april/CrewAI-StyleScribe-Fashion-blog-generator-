import os
from crewai import Crew, Process
from .agents import create_agents
from .tasks import create_suggestion_task, create_writing_tasks
from dotenv import load_dotenv

load_dotenv()

def run_topic_suggester(base_topic: str):
    """
    Runs a mini-crew with just the Researcher to generate 5 topic suggestions.
    """
    llm_name = "gpt-4o-mini"
    
    # We only need the researcher for this step, though create_agents returns all 3
    researcher, _, _ = create_agents(llm_name)
    
    suggestion_task = create_suggestion_task(researcher, base_topic)
    
    suggestion_crew = Crew(
        agents=[researcher],
        tasks=[suggestion_task],
        process=Process.sequential,
        verbose=True
    )
    
    result = suggestion_crew.kickoff()
    return str(result)

def run_fashion_crew(selected_topic: str, word_count: int):
    """
    Runs the full 3-agent crew to heavily research, format, and polish the blog post.
    """
    llm_name = "gpt-4o-mini"

    # Create Agents
    researcher, writer, editor = create_agents(llm_name)

    # Create Tasks with word count
    research_task, writing_task, editing_task = create_writing_tasks(
        researcher, writer, editor, selected_topic, word_count
    )

    # Form the Crew
    fashion_crew = Crew(
        agents=[researcher, writer, editor],
        tasks=[research_task, writing_task, editing_task],
        process=Process.sequential,
        verbose=True
    )

    # Execute the process
    result = fashion_crew.kickoff()
    return str(result)
