
import fitz  # PyMuPDF
import openai
import os
import re

openai.api_key = os.environ.get("OPENAI_API_KEY")

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    texts = [page.get_text() for page in doc]
    return texts

def chunk_text(text, max_length=1500):
    paragraphs = re.split(r'\n+', text)
    chunks, current_chunk = [], ""
    for para in paragraphs:
        if len(current_chunk) + len(para) < max_length:
            current_chunk += para + "\n"
        else:
            chunks.append(current_chunk.strip())
            current_chunk = para + "\n"
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def analyze_section(section_text, index):
    prompt = f"""
[슬라이드 내용]
{section_text}

[피드백 요청]
위 슬라이드의 내용을 바탕으로 제안서 피드백을 작성해주세요.
- 내용의 논리적 흐름과 설득력
- 오탈자 및 문법적 오류
- 더 나은 문장이나 구조에 대한 제안
- 빠진 내용이나 추가하면 좋을 요소
- 기타 제안 사항

[피드백]
"""
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "너는 매우 정확한 제안서 평가자야. 핵심을 집어 피드백하고 간결하게 작성해."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )
    return response.choices[0].message.content.strip()

def analyze_pdf(pdf_path):
    all_text = extract_text_from_pdf(pdf_path)
    sections = []
    for page_text in all_text:
        sections.extend(chunk_text(page_text))

    feedbacks = []
    for i, section in enumerate(sections):
        if len(section.strip()) < 100:
            continue
        feedback = analyze_section(section, i)
        feedbacks.append(f"--- Slide {i + 1} ---\n" + feedback)
    return "\n\n".join(feedbacks)
