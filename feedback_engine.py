import streamlit as st
import tempfile
import os
from feedback_engine import analyze_pdf, compare_documents

st.set_page_config(page_title="제안서 자동 피드백 시스템", layout="centered")

st.title("📄 제안서 자동 피드백 시스템")
mode = st.radio("분석 모드 선택", ["📑 단일 문서 피드백", "📂 문서 비교 분석"])

if mode == "📑 단일 문서 피드백":
    uploaded_file = st.file_uploader("PDF 파일을 업로드하세요", type="pdf")
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name
        
        with st.spinner("분석 중입니다..."):
            feedback = analyze_pdf(tmp_path)
        st.subheader("📋 분석 결과")
        st.write(feedback)
        os.unlink(tmp_path)

elif mode == "📂 문서 비교 분석":
    st.markdown("**기준 문서 (예: 제안요청서)**")
    base_file = st.file_uploader("", type="pdf", key="base")
    st.markdown("**비교할 문서 (예: 제안서)**")
    target_file = st.file_uploader(" ", type="pdf", key="target")

    if base_file and target_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_base:
            tmp_base.write(base_file.read())
            base_path = tmp_base.name

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_target:
            tmp_target.write(target_file.read())
            target_path = tmp_target.name

        with st.spinner("문서 비교 분석 중입니다..."):
            result = compare_documents(base_path, target_path)

        st.subheader("📋 비교 분석 결과")
        st.write(result)
        os.unlink(base_path)
        os.unlink(target_path)
