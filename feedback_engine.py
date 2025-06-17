
import fitz  # PyMuPDF
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def chunk_text(text, max_tokens=2000):
    chunks = []
    while len(text) > max_tokens:
        split_index = text.rfind(".", 0, max_tokens)
        if split_index == -1:
            split_index = max_tokens
        chunks.append(text[:split_index])
        text = text[split_index:]
    chunks.append(text)
    return chunks

def analyze_section(text, idx):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "당신은 문서를 분석해 개선사항을 제안하는 전문가입니다."},
            {"role": "user", "content": f"다음 제안서 내용을 읽고 피드백을 주세요:\n\n{text}"}
        ],
        temperature=0.4
    )
    return f"섹션 {idx+1} 피드백:\n" + response.choices[0].message.content

def analyze_pdf(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text)
    feedback = ""
    for i, section in enumerate(chunks):
        feedback += analyze_section(section, i) + "\n\n"
    return feedback

def compare_documents(base_path, target_path):
    base_text = extract_text_from_pdf(base_path)
    target_text = extract_text_from_pdf(target_path)
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "당신은 제안서를 평가하고 제안요청서와의 적합성을 분석하는 전문가입니다."},
            {"role": "user", "content": f"다음은 제안요청서입니다:\n\n{base_text}\n\n다음은 제안서입니다:\n\n{target_text}\n\n이 두 문서를 비교하여 제안서가 제안요청서에 얼마나 부합하는지 평가하고 개선점을 알려주세요."}
        ],
        temperature=0.4
    )
    return response.choices[0].message.content
