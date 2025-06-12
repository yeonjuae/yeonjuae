
import streamlit as st
import openai

st.set_page_config(page_title="GPT 슬라이드 피드백", layout="centered")

st.title("🧠 GPT 슬라이드 피드백")
st.markdown("슬라이드 제목과 본문을 입력하면, GPT가 자연어로 피드백을 제공합니다.")

title = st.text_input("슬라이드 제목", max_chars=100)
body = st.text_area("슬라이드 본문", height=200)

openai.api_key = "sk-test-vkAz5z1QtP7RbTtVqW3FT3BlbkFJwKIpUk7hx8RQqQbRpccD"

def generate_feedback(title, body):
    prompt = f'''
다음은 발표용 슬라이드의 제목과 본문입니다. 발표자가 슬라이드를 더 설득력 있게 만들 수 있도록 피드백을 해주세요.

[슬라이드 제목]
{title}

[슬라이드 본문]
{body}

[피드백]
'''
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"❌ 오류 발생: {e}"

if st.button("🔍 GPT 피드백 생성"):
    if title.strip() == "" or body.strip() == "":
        st.warning("제목과 본문을 모두 입력해주세요.")
    else:
        with st.spinner("GPT가 피드백을 작성 중입니다..."):
            feedback = generate_feedback(title, body)
            st.success("✅ 피드백 생성 완료")
            st.markdown("### 💬 GPT 피드백 결과")
            st.write(feedback)
