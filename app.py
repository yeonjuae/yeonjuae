
import streamlit as st
import tempfile
from feedback_engine import analyze_pdf, compare_documents

st.title("📄 제안서 자동 피드백 시스템")
mode = st.radio("분석 모드 선택", ["📑 단일 문서 피드백", "📂 문서 비교 분석"])

if mode == "📑 단일 문서 피드백":
    uploaded_file = st.file_uploader("PDF 파일 업로드", type=["pdf"])
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name
        feedback = analyze_pdf(tmp_path)
        st.subheader("📋 피드백 결과")
        st.write(feedback)

elif mode == "📂 문서 비교 분석":
    base_file = st.file_uploader("기준 문서 (예: 제안요청서)", type=["pdf"])
    target_file = st.file_uploader("비교할 문서 (예: 제안서)", type=["pdf"])
    if base_file and target_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp1, \
             tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp2:
            tmp1.write(base_file.read())
            tmp2.write(target_file.read())
            base_path, target_path = tmp1.name, tmp2.name
        result = compare_documents(base_path, target_path)
        st.subheader("📋 비교 분석 결과")
        st.write(result)
