# 🕵️ Agent Vinod - AI Interviewer Pro

Agent Vinod is an intelligent, voice-enabled AI hiring agent designed to conduct realistic technical and behavioral interviews. Built with Streamlit and Google Gemini, it analyzes resumes, conducts dynamic interviews, and provides detailed performance feedback with a strict grading rubric.

---

## 🚀 Key Features

🧠 Context-Aware: Upload a PDF resume, and the agent tailors questions to the candidate's specific projects and experience.
🎙️ Voice-First Interaction: Supports voice inputs (using the browser microphone) or text typing, simulating a real interview environment.
⚖️ Strict Grading Rubric:
    * 1-4: No Hire
    * 5-6: On the Fence
    * 7-8: Hire
    * 9-10: Strong Hire
⚡ High-Speed Architecture: Uses Google's Gemini 1.5 Flash model for low-latency responses.
🔒 Secure by Design: API keys are never hardcoded; they are handled via session-based UI input.

---

## 🛠️ Tech Stack

| Component | Technology | Reasoning |

| Frontend/UI | Streamlit | Allows for rapid prototyping of Chat UIs and handles audio widgets natively. |
| LLM Engine | Google Gemini API | Chosen for its high speed (flash model) and generous free tier compared to OpenAI. |
| Resume Parsing | PyPDF2 | Lightweight library to extract raw text from PDF resumes for context injection. |
| Audio Processing | hashlib | Used to fingerprint audio inputs to prevent Streamlit's re-run loop bug. |

---

## ⚙️ Installation & Setup

### Prerequisites
* Python 3.9 or higher
* A free Google Gemini API Key

### 1. Clone the Repository
#Bash
git clone [https://github.com/yourusername/agent-vinod.git](https://github.com/yourusername/agent-vinod.git)
cd agent-vinod

2. Create a Virtual Environment (Recommended)
Bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate

3. Install Dependencies
Create a requirements.txt file (if not present) with the following content:

streamlit
google-generativeai
PyPDF2
Then install them:

#Bash
pip install -r requirements.txt

4. Run the Application
#Bash
streamlit run interview_agent.py

🏗️ System Architecture
The application follows a State-Based Architecture using Streamlit's session_state. This ensures the bot remembers the conversation history despite the web page re-running on every interaction.

[Start: Setup Mode] --> [User Uploads Resume] | v [Initialize Agent Vinod] --> [Chat Loop] | v [User Speaks/Types] --> [Input Processing] --> [Hash Check] | (Is New Audio?) | | Yes No | | [Transcribe & Send to Gemini] [Ignore] | [Update Chat History]

💡 Design Decisions
1. The Ghost Input Fix (Hashlib)
Challenge: Streamlit re-runs the entire script whenever a user interacts with a widget. This caused the audio input to be re-processed on every refresh, making the bot reply to the same audio repeatedly.

Solution: I implemented hashlib.md5 to create a unique digital fingerprint of the audio bytes. The system only processes audio if the fingerprint differs from the previous turn.

2. UI-Based API Key Security
Challenge: Hardcoding API keys leads to security leaks if code is pushed to GitHub.

Solution: The app requests the API Key via the Sidebar UI. This ensures credentials exist only in the browser's temporary session memory (RAM) and are never saved to disk.

3. Text-Only Bot, Voice-Enabled User
Challenge: Full voice-to-voice (TTS) creates significant latency (3-5 seconds delay), breaking the flow of a high-pressure interview.

Solution: I opted for a Hybrid Approach. The user speaks (to prove communication skills), but the bot responds in text. This keeps the interview fast-paced and efficient, mimicking a live chat screening.

4. Strict JSON Feedback
Challenge: LLMs often give vague feedback like "Good job."

Solution: I used Prompt Engineering to force the model to output a strict JSON schema with a specific 1-10 grading rubric. This ensures consistent, actionable metrics for every candidate.

📂 Project Structure

/agent-vinod
│
├── interview_agent.py   # Main Application Logic
├── requirements.txt     # Python Dependencies
├── README.md            # Documentation
└── .gitignore           # Ignores venv and sensitive files

Built with ❤️ by Pranav Kashyap
