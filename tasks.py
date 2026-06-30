from crewai import Task


def create_resume_task(agent, resume_text, level):
    return Task(
        description=f"""
        Candidate Level:
        {level}
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


def create_next_question_task(
    agent,
    analysis,
    level,
    chat_history,
):
    return Task(
        description=f"""
        Candidate Level:
        {level}

        Resume Analysis:
        {analysis}

        Previous Interview History:
        {chat_history}

        You are conducting a real interview.

        Ask ONLY ONE question.

        Rules:
        - Natural interview flow
        - Use previous answers
        - Ask follow-up questions when needed
        - Increase difficulty if candidate performs well
        - Never ask multiple questions
        """,
        expected_output="A single interview question",
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
