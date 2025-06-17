
import fitz  # PyMuPDF
import openai
import os

def extract_text_from_pdf(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text()
    return text

def compare_documents(base_path, target_path):
    base_text = extract_text_from_pdf(base_path)
    target_text = extract_text_from_pdf(target_path)

    prompt = f"""다음은 두 개의 제안서 텍스트입니다.

[기준 제안서]
{base_text}

[비교 제안서]
{target_text}

두 문서를 항목별로 비교 분석하고, 비교 제안서가 기준 제안서에 비해 부족하거나 개선할 점이 있다면 구체적으로 제안해줘. 형식은 자유롭게 하되 명확하게."""

    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "너는 매우 정확하고 예리한 제안서 평가 전문가야."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )
    return response.choices[0].message.content
