
import streamlit as st
from feedback_engine import compare_documents
import tempfile

st.title("제안서 자동 피드백 시스템 (AI 기반)")

uploaded_files = st.file_uploader("PDF 파일 2개를 업로드하세요 (제안요청서, 제안서)", type=["pdf"], accept_multiple_files=True)

if uploaded_files and len(uploaded_files) == 2:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp1, tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp2:
        tmp1.write(uploaded_files[0].read())
        tmp2.write(uploaded_files[1].read())
        base_path = tmp1.name
        target_path = tmp2.name

    with st.spinner("GPT가 문서를 비교 분석 중입니다..."):
        result = compare_documents(base_path, target_path)

    st.subheader("🧠 피드백 결과")
    st.write(result)
else:
    st.info("⚠️ 제안요청서와 제안서를 각각 1개씩 업로드해 주세요.")
