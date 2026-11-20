#Crew Ai Demo
# Agents : Who performs the work?
# Tasks: what work needs to be completed?
# Crew : Which all agents gonna work together ?
#Process:in which order should they work?

from crewai import Agent, Task,Crew,Process
import os

os.environ["OPENAI_API_KEY"]="Your API Key"

#Research Agent :One Job ,Clear Task,Reusable
Researcher = Agent(
    role="Market Research",
    goal="find the competitors of Telsa",
    backstory="Ev Market expert",
    llm="gpt-4o-mini",
    vebose =True
)

#Analyze Agent
Analyst =Agent(
    role="Business Anlysis",
    goal="Analyse the strenths and weakness",
    backstory="Strategy consultant",
    llm="gpt-4o-mini",
    vebose =True
)

#Summarizer Agent
summariser =Agent(
    role="Report Writer",
    goal="Create a refined final report",
    backstory="Business Writer",
    llm="gpt-4o-mini",
    vebose =True
)

# Task 1
Research_task=Task(
    description="Identify Teslas Competitors",
    expected_output="""Competiros list and their vehicle list""",
    agent=Researcher
    )

# Task 2

Analyst_task =Task(
    description="Analyse the compettitors identified by researcher agent also evaluate the strengths and weakness",
    expected_output="""Competitors comparison with their strenghts and weaknesses""",
    agent=Analyst,
    context=[Research_task]
)

# Task 3
Summarize_task = Task(
    description="prepare a professional business report on Tesla's competitors",
    expected_output="""Compile a structured Business Report suitable for management audience""",
    agent=summariser,
    context=[Research_task,Analyst_task]

)

# Crew
crew= Crew(
    agents=[Researcher,Analyst,summariser],
    tasks=[Research_task,Analyst_task,Summarize_task],
    process=Process.sequential,
    verbose=True
)

# Run

result= crew.kickoff()
print(result)