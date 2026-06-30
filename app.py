import fitz
import streamlit as st
from crewai import Crew
from agents import (
    resume_analyzer,
    interviewer,
    evaluator,
)

from tasks import (
    create_resume_task,
    create_next_question_task,
    create_feedback_task,
)

MAX_QUESTIONS = 10

st.set_page_config(
    page_title="Mock Technical Interviewer",
    layout="wide",
)
st.title("Mock Technical Interviewer")

if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "current_question" not in st.session_state:
    st.session_state.current_question = None

if "question_count" not in st.session_state:
    st.session_state.question_count = 0

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "interview_started" not in st.session_state:
    st.session_state.interview_started = False

if "interview_finished" not in st.session_state:
    st.session_state.interview_finished = False

candidate_level = st.selectbox(
    "Experience Level",
    [
        "College Student / Fresher",
        "1-3 Years Experience",
        "3+ Years Experience",
    ],
)

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf"],
    max_upload_size=10
)

if uploaded_file and not st.session_state.interview_started:

    if st.button("Start Interview"):

        with st.spinner("Analyzing Resume..."):

            pdf = fitz.open(
                stream=uploaded_file.read(),
                filetype="pdf",
            )
            resume_text = ""
            for page in pdf:
                text = page.get_text("text")
                resume_text += text if isinstance(text, str) else ""

            task = create_resume_task(
                resume_analyzer,
                resume_text,
                candidate_level,
            )

            crew = Crew(
                agents=[resume_analyzer],
                tasks=[task],
            )

            analysis = crew.kickoff()
            st.session_state.analysis = str(analysis)

        with st.spinner("Generating First Question..."):

            task = create_next_question_task(
                interviewer,
                st.session_state.analysis,
                candidate_level,
                [],
            )

            crew = Crew(
                agents=[interviewer],
                tasks=[task],
            )

            first_question = crew.kickoff()

            st.session_state.current_question = str(first_question)

            st.session_state.interview_started = True

        st.rerun()


if st.session_state.interview_started and not st.session_state.interview_finished:

    st.markdown("---")
    st.subheader(f"Question {st.session_state.question_count + 1}/{MAX_QUESTIONS}")
    st.write(st.session_state.current_question)

    answer = st.text_area(
        "Your Answer",
        height=200,
        key=f"answer_{st.session_state.question_count}",
    )

    if st.button("Submit Answer"):

        if not answer.strip():
            st.warning("Please enter an answer.")
            st.stop()

        with st.spinner("Evaluating Answer..."):

            task = create_feedback_task(
                evaluator,
                st.session_state.current_question,
                answer,
            )

            crew = Crew(
                agents=[evaluator],
                tasks=[task],
            )

            feedback = crew.kickoff()

        st.session_state.chat_history.append(
            {
                "question": st.session_state.current_question,
                "answer": answer,
                "feedback": str(feedback),
            }
        )

        st.session_state.question_count += 1

        if st.session_state.question_count >= MAX_QUESTIONS:
            st.session_state.interview_finished = True
            st.rerun()

        with st.spinner("Generating Next Question..."):

            task = create_next_question_task(
                interviewer,
                st.session_state.analysis,
                candidate_level,
                st.session_state.chat_history,
            )

            crew = Crew(
                agents=[interviewer],
                tasks=[task],
            )

            next_question = crew.kickoff()

            st.session_state.current_question = str(next_question)

        st.rerun()

if st.session_state.interview_finished:

    st.success("Interview Completed")
    st.subheader("Interview Summary")

    for idx, item in enumerate(
        st.session_state.chat_history,
        start=1,
    ):
        with st.expander(f"Question {idx}"):
            st.markdown(f"**Question:** {item['question']}")
            st.markdown(f"**Answer:** {item['answer']}")
            st.markdown(f"**Feedback:**\n\n{item['feedback']}")

    if st.button("Start New Interview"):

        for key in list(st.session_state.keys()):
            del st.session_state[key]

        st.rerun()
