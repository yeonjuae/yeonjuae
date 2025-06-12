import streamlit as st
from feedback_engine import analyze_pdf
import tempfile

st.title("제안서 자동 피드백 시스템 (AI 기반)")

uploaded_file = st.file_uploader("제안서 PDF 업로드", type=["pdf"])
if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name
    with st.spinner("AI가 피드백을 생성 중입니다..."):
        feedback = analyze_pdf(tmp_path)
    st.subheader("🔍 피드백 결과")
    st.write(feedback)
