import streamlit as st
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from transformers import pipeline

load_dotenv()

# Page config
st.set_page_config(page_title="AI Research Agent", page_icon="🤖", layout="centered")

# Custom CSS
st.markdown("""
<style>
body {
    background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
    color: white;
}
.stTextInput>div>div>input {
    background-color: #1e1e1e;
    color: white;
}
.stButton button {
    background-color: #00c6ff;
    color: black;
    border-radius: 10px;
    padding: 10px;
}
.result-box {
    background-color: #1e1e1e;
    padding: 20px;
    border-radius: 10px;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align: center;'>🤖 AI Research Agent</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Search • Analyze • Summarize</p>", unsafe_allow_html=True)

# Input
query = st.text_input("🔍 Enter your topic")

if st.button("🚀 Generate Research"):

    if query:
        with st.spinner("🔍 Searching the web..."):
            tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
            response = tavily.search(query=query, max_results=3)
            data = " ".join([r["content"] for r in response["results"]])

        with st.spinner("🤖 Generating AI summary..."):
            summarizer = pipeline("text-generation", model="google/flan-t5-base")

            summary = summarizer(
                "Summarize this: " + data[:1000],
                max_new_tokens=150,
                do_sample=False
            )

            result = summary[0]['generated_text']
            result = result.replace("Summarize this:", "").strip()

        st.success("✅ Done!")

        # Result box
        st.markdown(f"<div class='result-box'>{result}</div>", unsafe_allow_html=True)

        # Save
        os.makedirs("output", exist_ok=True)
        with open("output/report.txt", "w", encoding="utf-8") as f:
            f.write(result)

    else:
        st.warning("⚠️ Please enter a topic")



        
        #py -3.11 -m streamlit run app.py