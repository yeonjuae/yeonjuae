
import streamlit as st
from feedback_engine import compare_documents
import tempfile

st.set_page_config(page_title="GPT 제안서 비교 피드백", layout="centered")
st.title("제안서 비교 분석 시스템 (AI 기반)")

uploaded_file_base = st.file_uploader("기준이 되는 제안서 PDF 업로드", type=["pdf"], key="base")
uploaded_file_target = st.file_uploader("비교할 제안서 PDF 업로드", type=["pdf"], key="target")

if uploaded_file_base and uploaded_file_target:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp1:
        tmp1.write(uploaded_file_base.read())
        base_path = tmp1.name

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp2:
        tmp2.write(uploaded_file_target.read())
        target_path = tmp2.name

    with st.spinner("GPT가 문서를 비교 분석 중입니다..."):
        result = compare_documents(base_path, target_path)

    st.subheader("🧠 피드백 결과")
    st.write(result)
