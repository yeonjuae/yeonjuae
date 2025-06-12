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

def compare_documents(base_path, target_path):
    base_text = extract_text_from_pdf(base_path)
    target_text = extract_text_from_pdf(target_path)

    prompt = f"""
[제안요청서 내용]
{base_text}

[제안서 내용]
{target_text}

위의 두 문서를 비교하여 제안서가 제안요청서의 요구사항을 얼마나 충실히 반영했는지 평가하고, 부족한 점과 개선점을 항목별로 3가지 이상 구체적으로 작성해주세요.
"""

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "너는 매우 정확한 제안서 평가 전문가야."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
    )
    return response.choices[0].message.content
