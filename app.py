
import streamlit as st
import tempfile
from feedback_engine import compare_documents

st.set_page_config(page_title="제안서 비교 피드백 시스템 (AI)", layout="centered")

st.title("📊 제안서 자동 피드백 (기준문서 기반 AI 비교)")

col1, col2 = st.columns(2)
with col1:
    base_file = st.file_uploader("📌 기준 문서 (예: 제안요청서)", type=["pdf"])
with col2:
    target_file = st.file_uploader("📝 제안서", type=["pdf"])

if base_file and target_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp1:
        tmp1.write(base_file.read())
        base_path = tmp1.name
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp2:
        tmp2.write(target_file.read())
        target_path = tmp2.name

    with st.spinner("GPT가 문서를 비교 분석 중입니다..."):
        result = compare_documents(base_path, target_path)
    st.subheader("🧠 피드백 결과")
    st.write(result)
else:
    st.info("기준 문서와 제안서를 모두 업로드해 주세요.")
