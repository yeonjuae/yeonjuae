
import fitz  # PyMuPDF
import openai
import os

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def compare_documents(base_path, target_path):
    base_text = extract_text_from_pdf(base_path)
    target_text = extract_text_from_pdf(target_path)

    prompt = f"""
다음은 제안요청서의 주요 내용입니다:

[제안요청서]
{base_text}

---

다음은 제안서입니다. 제안요청서와 비교했을 때 어떤 부분이 부족하거나 보완이 필요한지, 충실한지 항목별로 정리해 주세요:

[제안서]
{target_text}
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
