
import fitz
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_text(path):
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def compare_documents(base_path, target_path):
    base_text = extract_text(base_path)
    target_text = extract_text(target_path)

    prompt = f"""당신은 제안요청서를 기준으로 제안서를 평가하는 전문가입니다.

[기준 문서 내용]
{base_text}

[제안서 내용]
{target_text}

위 두 문서를 비교하여 다음 기준으로 피드백을 작성하세요:

1. 누락된 항목은 무엇인가요?
2. 제안서의 강점과 약점은?
3. 기준에 비해 미흡한 부분은?
4. 항목별 충족 여부 및 종합 의견

결과는 항목별로 보기 쉽게 정리하세요.
"""
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "너는 제안서 평가 전문가야."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )
    return response.choices[0].message.content
