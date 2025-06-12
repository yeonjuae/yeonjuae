
import fitz  # PyMuPDF
import openai
import os
import re

openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_sections_from_pdf(path):
    doc = fitz.open(path)
    sections = []
    for page in doc:
        text = page.get_text()
        sections.append(text)
    return sections

def analyze_section(text, index):
    prompt = f"""당신은 제안서 평가 전문가입니다. 아래는 제안서의 {index + 1}번째 섹션입니다. 제안요청서 기준에 따라 다음 항목을 평가하세요:

1. 요구사항 충족 여부 (O/X)
2. 내용의 구체성 (상/중/하)
3. 보완이 필요한 부분
4. 항목별 점수 (0~5점)

[제안서 내용]
{text}

[피드백]
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "너는 매우 정확한 제안서 평가 전문가야."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
    )
    return response['choices'][0]['message']['content']

def analyze_pdf(path):
    sections = extract_sections_from_pdf(path)
    feedbacks = []
    for i, section in enumerate(sections):
        if len(section.strip()) < 100:
            continue  # 너무 짧은 텍스트는 무시
        feedback = analyze_section(section, i)
        feedbacks.append(f"--- Slide {i + 1} ---\n" + feedback)
    return "\n\n".join(feedbacks)
