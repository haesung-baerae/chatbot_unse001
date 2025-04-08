import streamlit as st
import openai
from datetime import date
import re
import random
from streamlit.components.v1 import html
import urllib.parse
import textwrap
# OpenAI API 키 설정 (안전하게 보관할 땐 환경변수 사용 권장)
openai_api_key = st.secrets['openai']['API_KEY']
client = openai.OpenAI(api_key  = openai_api_key)
kakao_app_key = "e81bbaa2211fcf6024940d3cac85cc5b"


st.markdown("""
<a href="https://mature-cream-ear.glitch.me" target="_blank">
  <button style="
      padding: 10px 20px;
      font-size: 16px;
      background-color: #FEE500;
      color: #3C1E1E;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      font-weight: bold;">
    💬 카카오톡으로 공유하기
  </button>
</a>
""", unsafe_allow_html=True)


st.title("🔮 AI 오늘의 운세")
st.write("당신의 생년월일을 입력하면 AI가 오늘의 운세를 짧게!! 알려드립니다!")

# 생년월일 입력 받기
birth_date = st.date_input("📅 생년월일을 선택하세요", 
                           value=date(1990, 1, 1), 
                           min_value = date(1940, 1, 1),
                           max_value=date.today())

# 버튼 클릭 시 OpenAI에게 요청
if st.button("✨ 오늘의 운세 보기"):
    with st.spinner("운세를 점치는 중...🧙‍♂️"):
        # Prompt 생성
        today = date.today().strftime("%Y년 %m월 %d일")
        birth_str = birth_date.strftime("%Y년 %m월 %d일")
        prompt = (
            f"사용자의 생년월일은 {birth_str}이고, 오늘은 {today}입니다. "
            f"점성술사처럼 말투를 사용해서 오늘의 운세를 재미있고 긍정적으로 알려줘."
            f"3문장 정도로 간당하게 부탁해."
        )

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # 또는 "gpt-4"
                messages=[{"role": "user", "content": prompt}],
                temperature=0.9,
                max_tokens=200
            )

            result = response.choices[0].message.content
            # result는 GPT 응답 결과라고 가정
            sentences = re.split(r'(?<=[.!~])\s+', result)
            # 오늘 날짜
            today = date.today().strftime("%Y년 %m월 %d일")
            #st.markdown(f"📅 오늘은 **{today}**입니다.")

            # 오늘의 조언
            advice_list = [
                "🌿 여유를 가지고 깊게 숨 쉬어보세요.",
                "🔥 자신감을 가지면 길이 열립니다.",
                "🌈 오늘은 긍정적인 말을 한 마디 더 해보세요.",
                "🧘 주변 사람들에게 따뜻한 시선을 보내보세요.",
                "🌟 실패를 두려워하지 마세요, 모든 건 경험이 됩니다.",
                "💡 새로운 시도를 두려워하지 마세요.",
                "🍀 오늘 당신은 이미 충분히 잘하고 있어요."
            ]
            advice = random.choice(advice_list)
       
            # 👉 HTML에 Python 변수를 삽입
            content_html = f"""
            <div id="capture-area" style="
              background-color: #fff8f0;
              padding: 20px 30px;
              border-radius: 15px;
              box-shadow: 0 4px 10px rgba(0,0,0,0.1);
              font-size: 18px;
              line-height: 1.8;
              color: #5a3e36;
              width: 100%;
              max-width: 600px;
              margin: auto;
              box-sizing: border-box;
          ">

            <h2>🔮 오늘의 운세</h2>
            <p>📅 <strong>{today}</strong></p>
            <p>💡 <em>{advice}</em></p>
            <hr style="border: none; border-top: 1px solid #ccc; margin: 15px 0;" />
            {''.join(f"<p>👉 {line.strip()}</p>" for line in sentences if line.strip())}
            </div>

            <div style="text-align:center; margin-top: 20px;">
            <button onclick="downloadImage()" style="padding:10px 20px; font-size:16px; background-color:#6c5ce7; color:white; border:none; border-radius:8px; cursor:pointer;">📸 이미지로 저장</button>
            </div>

            <script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>
            <script>
            function downloadImage() {{
                const captureArea = document.getElementById("capture-area");
                html2canvas(captureArea).then(canvas => {{
                    const link = document.createElement("a");
                    link.download = "오늘의_운세.png";
                    link.href = canvas.toDataURL();
                    link.click();
                }});
            }}
            </script>
            """
            # Streamlit에 출력
            html(content_html, height=600)

            # URL 인코딩 처리
            encoded_result = urllib.parse.quote(result)
            
            # Glitch 공유 링크에 메시지 실어보내기
            glitch_url = f"https://mature-cream-ear.glitch.me/?message={encoded_result}"
            
            st.markdown(
                f'<a href="{glitch_url}" target="_blank">'
                '<button style="padding:10px 20px; font-size:16px; background-color:#FEE500; '
                'color:#3C1E1E; border:none; border-radius:8px; cursor:pointer; font-weight:bold;">'
                '💬 나의 운세 공유하기</button></a>',
                unsafe_allow_html=True
            )
          
            
        except Exception as e:
            st.error(f"에러 발생: {e}")
