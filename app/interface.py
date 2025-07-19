import sys
import os
import asyncio
sys.path.append(os.path.abspath("."))

import streamlit as st
from app.explainer import generate_explanation
from app.feedback import submit_feedback

# 🔧 Page config
st.set_page_config(page_title="🕵️‍♂️ VraTA - Fake News Classifier", layout="wide")

# 🎨 Custom CSS Styling
st.markdown("""
    <style>
        body { background-color: #0f1117; color: #f1f3f6; }
        .stTextArea textarea {
            background-color: #1e1e28 !important;
            color: #f1f3f6 !important;
            border-radius: 10px;
        }
        .stButton button {
            background-color: #0066cc;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 16px;
            font-weight: bold;
        }
        .stMarkdown, .stSubheader { color: #f1f3f6 !important; }
        .stCodeBlock {
            background-color: #12151c !important;
            color: #dcdcdc;
        }
        .stAlert {
            background-color: #252a36;
            color: #f1f3f6;
        }
        nav {
            text-align: center;
            margin-bottom: 20px;
        }
        nav a {
            margin: 0 20px;
            color: #ccc;
            font-weight: bold;
            text-decoration: none;
        }
        nav a:hover { color: white; }
    </style>
""", unsafe_allow_html=True)

# 🧭 Navbar
st.markdown("""
<nav>
    <a href="#">🏠 Home</a>
    <a href="#">📢 Feedback</a>
    <a href="#">👨‍💻 About</a>
</nav>
""", unsafe_allow_html=True)

# 🧠 App Title
st.markdown("<h1 style='text-align: center;'>🕵️‍♀️ VraTA</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>AI-Powered Real vs Fake News Classifier</p>", unsafe_allow_html=True)

# 📝 User Input
statement = st.text_area("📰 Enter a news statement to verify", height=150)

# 🧠 Run Inference
if st.button("🔍 Analyze Now"):
    if not statement.strip():
        st.warning("Please enter a news statement to analyze.")
    else:
        with st.spinner("🔎 Classifying and retrieving facts..."):
            result = asyncio.run(generate_explanation(statement, verdict=None))  # ⬅️ async support

        # 📌 Verdict Badge
        verdict = result["verdict"]
        verdict_color = "green" if verdict.lower() == "real" else "red"
        st.subheader("📌 Verdict")
        st.markdown(f"""
        <span style='
            padding: 6px 14px;
            border-radius: 10px;
            background-color: {verdict_color};
            color: white;
            font-weight: bold;
        '>🧾 Verdict: {verdict}</span>
        """, unsafe_allow_html=True)

        # 📊 Confidence Bar
        st.markdown(f"**Confidence:** `{result['confidence']}%`")
        st.progress(min(int(result["confidence"]), 100))

        # 🧠 Explanation
        st.subheader("🧠 Explanation")
        st.info(result["explanation"])

        # 🔎 Context
        st.subheader("🔎 Supporting Context")
        st.code(result["retrieved_context"], language="markdown")

        # 📢 Feedback
        st.subheader("📢 Feedback")
        feedback = st.radio("Do you agree with the verdict?", ["Yes", "No"])
        if feedback == "No":
            user_verdict = st.selectbox("What should it be?", ["Fake", "Real"])
            reason = st.text_area("Why do you disagree?")
            if st.button("📤 Submit Feedback"):
                submit_feedback(statement, result["verdict"], user_verdict, reason)
                st.success("✅ Feedback submitted! Thank you.")
