
import streamlit as st
import requests

st.set_page_config(page_title="제안서 피드백 생성기", layout="centered")

# Groq API 키 (Streamlit secrets에서 불러오기)
api_key = st.secrets["groq_api_key"]

def ask_groq(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mixtral-8x7b-32768",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    return result['choices'][0]['message']['content']

# Streamlit UI
st.title("📄 제안서 피드백 생성기")
st.markdown("Streamlit + Groq API를 사용한 제안서 비교 피드백 자동 생성기입니다.")

user_input = st.text_area(
    "비교 내용 또는 피드백 요약",
    placeholder="예: 제안서에서 3.1 요구사항이 누락되었습니다.",
    height=200
)

if st.button("피드백 문장 생성"):
    if user_input.strip() == "":
        st.warning("입력 내용을 작성해주세요.")
    else:
        with st.spinner("Groq에게 요청 중..."):
            prompt = f"다음 내용을 바탕으로 제안서 피드백 문장을 전문가처럼 자연스럽게 작성해줘:

{user_input}"
            output = ask_groq(prompt)
        st.success("완료!")
        st.markdown("### ✍️ 생성된 피드백 문장:")
        st.write(output)
