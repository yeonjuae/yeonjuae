import fitz  # PyMuPDF
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def split_into_sections(text, max_length=1500):
    paragraphs = text.split("\n")
    sections = []
    current = ""
    for para in paragraphs:
        if len(current) + len(para) < max_length:
            current += para + "\n"
        else:
            sections.append(current)
            current = para + "\n"
    if current:
        sections.append(current)
    return sections

def analyze_section(section, index=0):
    prompt = f"""아래는 제안서의 일부입니다. 이 내용을 검토하여 보완할 점이나 아쉬운 점이 있다면 작성해 주세요.

[내용]
{section}

[피드백]"""

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "너는 매우 정확한 제안서 평가 전문가야. 문서에서 아쉬운 점을 조목조목 피드백해줘."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
    )
    return response.choices[0].message.content.strip()

def analyze_pdf(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    sections = split_into_sections(text)
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

    prompt = f"""다음은 기준 문서와 비교 대상 문서입니다. 두 문서의 차이점을 분석하고, 새 문서의 보완할 점을 알려주세요.

[기준 문서]
{base_text}

[비교 대상 문서]
{target_text}

[피드백]"""

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "너는 전문 제안서 리뷰어야. 두 문서를 비교해서 차이점과 부족한 점을 알려줘."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
    )
    return response.choices[0].message.content.strip()