import streamlit as st
from feedback_engine import analyze_pdf, compare_documents
import tempfile

st.set_page_config(page_title="제안서 자동 피드백 시스템", layout="centered")
st.title("📄 제안서 자동 피드백 시스템")

tab1, tab2 = st.tabs(["📑 단일 문서 피드백", "📂 문서 비교 분석"])

with tab1:
    uploaded_file = st.file_uploader("제안서 PDF 업로드", type=["pdf"], key="single")
    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name

        with st.spinner("AI가 피드백을 생성 중입니다..."):
            feedback = analyze_pdf(tmp_path)

        st.subheader("🔍 피드백 결과")
        st.write(feedback)

with tab2:
    base_file = st.file_uploader("기준 문서 업로드", type=["pdf"], key="base")
    target_file = st.file_uploader("비교 대상 문서 업로드", type=["pdf"], key="target")

    if base_file and target_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp1,              tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp2:
            tmp1.write(base_file.read())
            base_path = tmp1.name

            tmp2.write(target_file.read())
            target_path = tmp2.name

        with st.spinner("GPT가 문서를 비교 분석 중입니다..."):
            result = compare_documents(base_path, target_path)

        st.subheader("🧠 피드백 결과")
        st.write(result)