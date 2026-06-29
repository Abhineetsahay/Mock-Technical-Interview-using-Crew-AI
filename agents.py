import os
from dotenv import load_dotenv
from crewai import Agent, LLM

import crewai.llms.cache as _crewai_cache

# Disable cache breakpoint injection
_crewai_cache.mark_cache_breakpoint = lambda msg: msg
load_dotenv()

llm = LLM(model="groq/llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))

resume_analyzer = Agent(
    role="Resume Analyzer",
    goal="Analyze resumes and identify skills, projects, strengths and weakness",
    backstory="A Senior Technical Recuriter",
    llm=llm,
    allow_delegation=True,
)

interviewer = Agent(
    role="Technical Interviewer",
    goal="Generate questions for the interview based on the resume",
    backstory="A Senior Software Engineer",
    llm=llm,
    allow_delegation=True,
)

evaluator = Agent(
    role="Interview Evaluator",
    goal="Evaluate candidate answers and provide feedback.",
    backstory="Experienced engineering manager.",
    llm=llm,
)