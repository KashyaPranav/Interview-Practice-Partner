import streamlit as st
import google.generativeai as genai
import hashlib
import json
import PyPDF2

st.set_page_config(page_title="Agent Vinod", page_icon="🕵️", layout="wide")

with st.sidebar:
    st.title("⚙️ Mission Control")
    gemini_key = st.text_input("🔑 Gemini API Key", type="password")
    
    if not gemini_key:
        st.warning("⚠️ Please enter your API key to activate Agent Vinod.")
        st.stop()
    
    try:
        genai.configure(api_key=gemini_key)
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        model_choice = st.selectbox("🧠 AI Model", models)
    except Exception as e:
        st.error(f"❌ Connection failed: {e}")
        st.stop()

    st.divider()
    st.header("📋 Candidate Profile")
    job_role = st.text_input("🎯 Target Role", value="Software Engineer")
    exp_level = st.selectbox("📈 Experience Level", ["Junior", "Mid-Level", "Senior"])
    
    pdf_file = st.file_uploader("📄 Upload Resume (Optional)", type="pdf")
    resume_content = ""
    
    if pdf_file:
        try:
            reader = PyPDF2.PdfReader(pdf_file)
            for page in reader.pages:
                resume_content += page.extract_text()
            st.success("✅ Resume Intelligence Loaded")
        except:
            st.error("❌ Could not parse PDF")

    if st.button("🔄 Reset Mission"):
        st.session_state.clear()
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "audio_hash" not in st.session_state:
    st.session_state.audio_hash = None
if "app_mode" not in st.session_state:
    st.session_state.app_mode = "start"

def get_transcription(audio_data):
    model = genai.GenerativeModel(model_choice)
    try:
        response = model.generate_content([
            "Transcribe this audio text exactly as spoken.",
            {"mime_type": "audio/wav", "data": audio_data}
        ])
        return response.text
    except:
        return None

def analyze_performance(conversation_text):
    model = genai.GenerativeModel(model_choice)
    prompt = f"""
    Analyze this interview transcript for a {job_role} position.
    Transcript:
    {conversation_text}
    
    Use this strict grading rubric for the score and decision:
    - 1-4: No Hire (Major knowledge gaps).
    - 5-6: No Hire / On the Fence (Weak answers).
    - 7-8: Hire (Competent, meets requirements).
    - 9-10: Strong Hire (Exceptional).
    
    Return a valid JSON object with these keys:
    - score: integer (1-10)
    - decision: string (Based on the rubric above)
    - tone: string
    - strengths: list of strings
    - weaknesses: list of strings
    - summary: string
    """
    try:
        res = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
        return json.loads(res.text)
    except:
        return None

if st.session_state.app_mode == "start":
    st.title("🕵️ Agent Vinod")
    st.subheader("🚀 Your elite AI Hiring Agent for technical and behavioral screening.")
    
    st.write(f"Ready to evaluate your skills for the **{job_role}** position. Upload your resume for a targeted drill.")
    
    if st.button("⚡ Start Interview"):
        st.session_state.app_mode = "chat"
        
        instruction = f"""
        You are Agent Vinod, an expert AI Hiring Manager for a {exp_level} {job_role} role.
        Context from Candidate Resume: {resume_content}
        
        Conduct a professional, sharp, and structured interview. 
        Ask one question at a time.
        Tailor questions to the resume if provided.
        Do not provide feedback yet.
        """
        
        model = genai.GenerativeModel(model_choice, system_instruction=instruction)
        st.session_state.chat_session = model.start_chat(history=[])
        
        greeting = f"Hello. I am Agent Vinod. I reviewed your profile for the {job_role} position. Let's begin. Please introduce yourself."
        st.session_state.messages.append({"role": "assistant", "content": greeting})
        st.rerun()

elif st.session_state.app_mode == "chat":
    st.title("🕵️ Agent Vinod is Interviewing...")
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            
    st.divider()
    c1, c2 = st.columns([4, 1])
    
    with c1:
        user_txt = st.chat_input("Type your answer...")
    with c2:
        user_audio = st.audio_input("🎙️ Speak Answer")
        
    final_response = None
    
    if user_txt:
        final_response = user_txt
    elif user_audio:
        raw_bytes = user_audio.read()
        cur_hash = hashlib.md5(raw_bytes).hexdigest()
        
        if cur_hash != st.session_state.audio_hash:
            st.session_state.audio_hash = cur_hash
            with st.spinner("🎧 Agent Vinod is listening..."):
                final_response = get_transcription(raw_bytes)

    if final_response:
        st.session_state.messages.append({"role": "user", "content": final_response})
        
        with st.spinner("🤔 Evaluating..."):
            try:
                ai_resp = st.session_state.chat_session.send_message(final_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_resp.text})
                st.rerun()
            except Exception as e:
                st.error(f"System Error: {e}")

    if len(st.session_state.messages) > 2:
        if st.button("🏁 End & Generate Report", type="primary"):
            st.session_state.app_mode = "report"
            st.rerun()

elif st.session_state.app_mode == "report":
    st.title("📊 Mission Report")
    
    full_text = ""
    for m in st.session_state.messages:
        full_text += f"{m['role'].upper()}: {m['content']}\n"
        
    with st.spinner("📝 Compiling performance dossier..."):
        data = analyze_performance(full_text)
        
        if data:
            col1, col2, col3 = st.columns(3)
            col1.metric("🏆 Score", f"{data.get('score', 0)}/10")
            col2.metric("⚖️ Verdict", data.get('decision', 'N/A'))
            col3.metric("🗣️ Tone", data.get('tone', 'N/A'))
            
            st.divider()
            st.subheader("📋 Executive Summary")
            st.info(data.get('summary', ''))
            
            c1, c2 = st.columns(2)
            with c1:
                st.success("✅ Strengths")
                for s in data.get('strengths', []):
                    st.write(f"• {s}")
            with c2:
                st.warning("⚠️ Areas for Growth")
                for w in data.get('weaknesses', []):
                    st.write(f"• {w}")
        else:
            st.error("Failed to generate report. Please try again.")
            
    if st.button("🔄 Start New Mission"):
        st.session_state.clear()
        st.rerun()