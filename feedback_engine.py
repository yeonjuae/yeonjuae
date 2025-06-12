import fitz  # PyMuPDF
import openai
import os

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def split_text_by_sections(text, max_length=2000):
    sections = []
    while len(text) > max_length:
        split_index = text[:max_length].rfind("\n")
        if split_index == -1:
            split_index = max_length
        sections.append(text[:split_index])
        text = text[split_index:]
    sections.append(text)
    return sections

def compare_documents(base_pdf, target_pdf):
    base_text = extract_text_from_pdf(base_pdf)
    target_text = extract_text_from_pdf(target_pdf)

    sections = split_text_by_sections(target_text)
    feedbacks = []

    for i, section in enumerate(sections):
        if len(section.strip()) < 100:
            continue

        prompt = f"""[제안요청서]
{base_text}

[제안서 일부 내용]
{section}

위 제안서 내용이 제안요청서의 조건에 얼마나 부합하는지 평가하고, 잘된 점과 개선점을 명확하게 작성해줘.

[피드백]"""

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "너는 매우 정확한 제안서 평가 전문가야. 제안요청서 기준에 맞춰 평가해줘."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
        )
        feedbacks.append(f"--- Slide {i + 1} ---\n" + response.choices[0].message.content)

    return "\n\n".join(feedbacks)
