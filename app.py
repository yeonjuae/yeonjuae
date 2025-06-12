import streamlit as st
from feedback_engine import compare_documents
import tempfile

st.set_page_config(page_title="GPT 슬라이드 피드백", layout="centered")
st.title("제안서 자동 피드백 시스템 (AI 기반)")

st.markdown("두 개의 PDF 문서를 업로드하면 AI가 차이점과 개선점을 분석해드립니다.")

base_file = st.file_uploader("📄 제안요청서 (PDF)", type=["pdf"])
target_file = st.file_uploader("📝 제안서 (PDF)", type=["pdf"])

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
