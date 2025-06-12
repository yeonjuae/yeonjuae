from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_section(section, index):
    prompt = f"""
    [슬라이드 {index+1} 내용]
    {section}

    [피드백]
    위 내용을 바탕으로 잘된 점과 개선할 점을 자세하게 작성해줘.
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "너는 제안서 평가 전문가야."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
    )
    return response.choices[0].message.content
