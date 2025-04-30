from crewai import Agent, Task, Crew
from composio_crewai import ComposioToolSet, Action
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Composio toolset
composio_toolset = ComposioToolSet(
    api_key=os.getenv("COMPOSIO_API_KEY"),
)

# Get GitHub star repo tool
github_tools = composio_toolset.get_tools(
    actions=['GITHUB_STAR_A_REPOSITORY_FOR_THE_AUTHENTICATED_USER']
)

# Configure Groq LLM
from langchain_groq import ChatGroq
groq_llm = ChatGroq(
    model="groq/llama-3.3-70b-versatile",
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY"),
)

# Define agent
github_agent = Agent(
    role="GitHub Star Repo Agent",
    goal="Star GitHub repositories for the authenticated user",
    backstory=(
        "You are an AI agent responsible for starring GitHub repositories for the authenticated user."
    ),
    verbose=True,
    tools=github_tools,
    llm=groq_llm,
    allow_delegation=False
)

# Define task
github_task = Task(
    description="Star a GitHub repository for the authenticated user",
    agent=github_agent,
    expected_output="Confirmation that the repository was starred successfully",
    async_execution=False
)

# Initialize crew
github_crew = Crew(
    agents=[github_agent],
    tasks=[github_task],
    process="sequential",
    memory=False,
    max_rpm=3
)

