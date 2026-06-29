import fitz
import streamlit as st

from crewai import Crew

from agents import resume_analyzer, interviewer, evaluator

from tasks import create_resume_task, create_question_task, create_feedback_task

st.title("Mock Technical Interviewer")

uploaded_file = st.file_uploader("Upload Resume", type=["pdf"])

if uploaded_file:

    pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")

    resume_text = ""

    for page in pdf:
        text = page.get_text("text")
        resume_text += text if isinstance(text, str) else ""

    if st.button("Analyze Resume"):

        task = create_resume_task(resume_analyzer, resume_text)

        crew = Crew(agents=[resume_analyzer], tasks=[task])

        analysis = crew.kickoff()

        st.session_state.analysis = str(analysis)

        st.subheader("Resume Analysis")
        st.write(analysis)

if "analysis" in st.session_state:

    if st.button("Generate Questions"):

        task = create_question_task(interviewer, st.session_state.analysis)

        crew = Crew(agents=[interviewer], tasks=[task])

        questions = crew.kickoff()

        st.session_state.questions = str(questions)

        st.subheader("Interview Questions")
        st.write(questions)
        print(questions)

if "questions" in st.session_state:

    questions = [
        q.strip() for q in st.session_state["questions"].split("\n") if q.strip()
    ]

    answers = []

    st.subheader("Answer the Questions")

    for i, q in enumerate(questions, start=1):
        st.markdown(f"### Question {i}")
        st.write(q)

        ans = st.text_area(f"Your Answer {i}", key=f"answer_{i}", height=120)

        answers.append(ans)

    if st.button("Evaluate Answers"):

        combined_feedback = []

        for i, (q, ans) in enumerate(zip(questions, answers), start=1):

            task = create_feedback_task(evaluator, q, ans)

            crew = Crew(agents=[evaluator], tasks=[task])

            feedback = crew.kickoff()

            combined_feedback.append(f"## Question {i}\n{feedback}")

        st.subheader("Feedback")
        st.markdown("\n\n".join(combined_feedback))
