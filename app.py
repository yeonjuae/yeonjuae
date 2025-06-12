import streamlit as st
from feedback_engine import compare_documents
import tempfile

st.title("제안서 자동 피드백 시스템 (AI 기반)")

base_file = st.file_uploader("📄 [1] 제안요청서 PDF 업로드", type=["pdf"])
uploaded_file = st.file_uploader("📝 [2] 제안서 PDF 업로드", type=["pdf"])

if base_file and uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False) as tmp1:
        tmp1.write(base_file.read())
        base_path = tmp1.name

    with tempfile.NamedTemporaryFile(delete=False) as tmp2:
        tmp2.write(uploaded_file.read())
        target_path = tmp2.name

    with st.spinner("GPT가 문서를 비교 분석 중입니다..."):
        result = compare_documents(base_path, target_path)

    st.subheader("🧠 피드백 결과")
    st.write(result)
