# Mock Technical Interviewer

A simple AI-powered Mock Technical Interviewer built using CrewAI, Streamlit, and Groq.

The application analyzes a candidate's resume, generates interview questions based on their profile, and evaluates their answers with personalized feedback.

## Features

- Upload Resume (PDF)
- AI Resume Analysis
- Technical Interview Question Generation
- Answer Evaluation
- Personalized Feedback
- Multi-Agent Workflow using CrewAI

## Tech Stack

- Python
- Streamlit
- CrewAI
- Groq LLM
- PyMuPDF

## Project Structure

```text
mock_interviewer/
│
├── app.py
├── agents.py
├── tasks.py
├── requirements.txt
├── .env
└── README.md
```

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd mock_interviewer
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_groq_api_key
```

## Run Application

```bash
streamlit run app.py
```

## Workflow

1. Upload your resume in PDF format.
2. AI analyzes the resume and identifies skills, projects, strengths, and improvement areas.
3. Generate technical interview questions based on the analysis.
4. Submit answers to interview questions.
5. Receive AI-generated evaluation and feedback.
