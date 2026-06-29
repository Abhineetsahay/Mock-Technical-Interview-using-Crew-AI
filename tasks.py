from crewai import Task


def create_resume_task(agent, resume_text):
    return Task(
        description=f"""
        Analyze the following resume:

        {resume_text}

        Extract:
        1. Skills
        2. Projects
        3. Strengths
        4. Weaknesses
        5. 5 interview topics
        """,
        expected_output="Detailed resume analysis.",
        agent=agent,
    )


def create_question_task(agent, analysis):
    return Task(
        description=f"""
        Based on the resume analysis below:

        {analysis}

        Generate 10 technical interview questions.
        """,
        expected_output="List of interview questions.",
        agent=agent,
    )


def create_feedback_task(agent, question, answer):
    return Task(
        description=f"""
        Question:
        {question}

        Candidate Answer:
        {answer}

        Evaluate:
        - Technical Accuracy
        - Communication
        - Completeness

        Give score out of 10 and improvement suggestions.
        """,
        expected_output="Evaluation report.",
        agent=agent,
    )
