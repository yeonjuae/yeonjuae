
import openai
import streamlit as st
from PyPDF2 import PdfReader

openai.api_key = st.secrets["OPENAI_API_KEY"]

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    return "\n".join(page.extract_text() for page in reader.pages if page.extract_text())

def analyze_section(text, idx):
    prompt = f"다음은 제안서의 섹션 {idx+1} 내용입니다:\n{text}\n\n이 내용에 대해 구체적인 피드백을 작성해주세요."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "너는 제안서를 분석해주는 전문가야."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )
    return response.choices[0].message.content

def analyze_pdf(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    sections = text.split("\n\n")
    feedbacks = []
    for i, section in enumerate(sections):
        if len(section.strip()) < 100:
            continue
        feedback = analyze_section(section, i)
        feedbacks.append(f"--- Slide {i + 1} ---\n" + feedback)
    return "\n\n".join(feedbacks)

def compare_documents(base_path, target_path):
    base_text = extract_text_from_pdf(base_path)
    target_text = extract_text_from_pdf(target_path)
    prompt = f"기준 문서:\n{base_text}\n\n비교 대상 문서:\n{target_text}\n\n두 문서를 비교하고 부족한 부분에 대한 피드백을 작성해줘."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "너는 제안서를 비교 분석하는 전문가야."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )
    return response.choices[0].message.content
