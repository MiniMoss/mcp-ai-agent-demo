from crewai import Agent, Task, Crew
from langchain_groq import ChatGroq
from composio_crewai import ComposioToolSet, Action
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Composio toolset
composio_toolset = ComposioToolSet(
    api_key=os.getenv("COMPOSIO_API_KEY"),
)

# Get Gmail send email tool
tools = composio_toolset.get_tools(
    actions=[Action.GMAIL_SEND_EMAIL]
)

# Configure Groq LLM
groq_llm = ChatGroq(
    model="groq/llama-3.3-70b-versatile",
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY"),
)

# Define agent
crewai_agent = Agent(
    role="Gmail Email Sender",
    goal="Send emails via Gmail API",
    backstory=(
        "You are a professional email-sending assistant, "
        "capable of sending emails accurately using the Gmail API."
    ),
    verbose=True,
    tools=tools,
    llm=groq_llm,
    allow_delegation=False
)

# Define task
task = Task(
    description="Send an email based on provided recipient, subject, and body",
    agent=crewai_agent,
    expected_output="Confirmation that the email was sent successfully",
    async_execution=False
)

# Initialize crew
my_crew = Crew(
    agents=[crewai_agent],
    tasks=[task],
    process="sequential",
    memory=False,
    max_rpm=3
)