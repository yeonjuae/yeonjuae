# app.py
import streamlit as st
from feedback_engine import analyze_pdf, compare_documents
import tempfile

st.set_page_config(page_title="제안서 자동 피드백 시스템", layout="centered")
st.title("📄 제안서 자동 피드백 시스템")

mode = st.radio("분석 모드 선택", ["📑 단일 문서 피드백", "📂 문서 비교 분석"])

if mode == "📑 단일 문서 피드백":
    uploaded_file = st.file_uploader("제안서 PDF 업로드", type=["pdf"])

    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name

        with st.spinner("AI가 피드백을 생성 중입니다..."):
            feedback = analyze_pdf(tmp_path)
        st.subheader("🔍 피드백 결과")
        st.write(feedback)

else:
    base = st.file_uploader("기준 문서 (예: 제안요청서)", type=["pdf"], key="base")
    target = st.file_uploader("비교할 문서 (예: 제안서)", type=["pdf"], key="target")

    if base and target:
        with tempfile.NamedTemporaryFile(delete=False) as tmp1:
            tmp1.write(base.read())
            base_path = tmp1.name

        with tempfile.NamedTemporaryFile(delete=False) as tmp2:
            tmp2.write(target.read())
            target_path = tmp2.name

        with st.spinner("GPT가 문서를 비교 분석 중입니다..."):
            result = compare_documents(base_path, target_path)
        st.subheader("🧠 피드백 결과")
        st.write(result)
