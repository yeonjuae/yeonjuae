
# GPT 제안서 피드백 시스템

## 설명
이 프로젝트는 제안요청서와 제안서를 함께 업로드하면 GPT가 비교하여 자동 피드백을 생성해주는 Streamlit 웹앱입니다.

## 실행 방법
```
pip install -r requirements.txt
streamlit run app.py
```

## 배포 방법
Streamlit Community Cloud에서 배포 시, Secrets에 아래 환경변수를 추가하세요:

```
OPENAI_API_KEY = "your-key"
```
