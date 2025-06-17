
import fitz  # PyMuPDF
import openai
import os
import re

openai.api_key = os.environ.get("OPENAI_API_KEY")

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def split_sections(text):
    slides = re.split(r"(?i)(?=slide \d+:?)", text)
    return [slide.strip() for slide in slides if slide.strip()]

def analyze_section(section, index):
    prompt = f"""
너는 매우 정확한 제안서 평가자야. 아래는 슬라이드 {index + 1}의 내용이야. 논리성, 명확성, 설득력을 기준으로 평가하고, 수정이나 개선이 필요한 부분이 있다면 구체적으로 설명해줘.

[슬라이드 내용]
{section}

[피드백]
"""
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "너는 매우 정확한 제안서 평가자야."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
    )
    return response.choices[0].message.content

def analyze_pdf(file_path):
    text = extract_text_from_pdf(file_path)
    sections = split_sections(text)
    feedbacks = []
    for i, section in enumerate(sections):
        if len(section.strip()) < 100:
            continue
        feedback = analyze_section(section, i)
        feedbacks.append(f"--- Slide {i + 1} ---\n" + feedback)
    return "\n\n".join(feedbacks)
