# 제안서 자동 피드백 시스템

이 프로젝트는 제안요청서 기준에 따라 사용자가 업로드한 제안서를 분석하고 GPT를 활용해 피드백을 제공합니다.

## 실행 방법
1. GitHub에 업로드 후 [Streamlit Cloud](https://streamlit.io/cloud)에 연결
2. main file: `app.py`
3. 필요 라이브러리: `requirements.txt` 참고
4. 환경 변수에 `OPENAI_API_KEY` 등록 필요

## 사용 흐름
- 사용자는 PDF 파일 업로드
- 시스템은 텍스트 추출 및 분석
- GPT가 기준 문서 기반 피드백 생성
