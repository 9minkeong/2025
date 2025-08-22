import streamlit as st
import time

# 페이지 설정
st.set_page_config(page_title="💊 증상별 약 추천", page_icon="💊", layout="wide")

# CSS 스타일링
st.markdown("""
    <style>
    .stApp {
        background-color: #F0F8FF;
    }
    .card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 3px 3px 20px rgba(0,0,0,0.1);
        margin-bottom: 25px;
    }
    .title {
        color: #4B0082;
        text-align: center;
    }
    .highlight {
        color: #FF4500;
        font-weight: bold;
    }
    .emoji {
        font-size: 50px;
        text-align: center;
        animation: pop 0.5s ease-in-out;
    }
    @keyframes pop {
        0% {transform: scale(0);}
        50% {transform: scale(1.5);}
        100% {transform: scale(1);}
    }
    </style>
""", unsafe_allow_html=True)

# 상단 제목
st.markdown("<h1 class='title'>💊 증상별 약 추천 & 관리법</h1>", unsafe_allow_html=True)
st.write("⚠️ 이 앱은 의료 참고용입니다. 정확한 진단은 반드시 의사·약사에게 받으세요.")

# 데이터베이스
medicine_dict = {
    "두통": {
        "약": "진통제 (예: 타이레놀, 이부프로펜)",
        "부작용": "속쓰림, 위장 장애",
        "관리법": "충분한 수분 섭취, 눈 휴식, 규칙적인 수면",
        "복용시간": "증상 발생 시, 하루 최대 4회",
        "주의사항": "간 질환이 있는 경우 복용 전 의사 상담",
        "복용팁": "공복보다는 식후 복용이 위장 부담을 줄여줍니다."
    },
    "발열": {
        "약": "해열제 (예: 아세트아미노펜, 이부프로펜)",
        "부작용": "간 손상(과량 복용 시), 위장 장애, 드물게 알러지 반응",
        "관리법": "충분한 수분 섭취, 가벼운 옷 착용, 휴식, 체온 모니터링",
        "복용시간": "6~8시간 간격으로 필요 시 복용",
        "주의사항": "어린이, 노인, 간 질환자 주의",
        "복용팁": "체온이 38도 이상일 때 필요시 복용, 하루 최대 용량 준수"
    },
    "기침": {
        "약": "진해제, 거담제 (예: 덱스트로메토르판, 암브록솔)",
        "부작용": "졸림, 어지럼증, 장기간 사용 시 의존 가능",
        "관리법": "따뜻한 음료 섭취, 실내 습도 유지, 충분한 휴식",
        "복용시간": "하루 2~3회, 필요 시 복용",
        "주의사항": "만 2세 이하 아동은 사용 제한",
        "복용팁": "밤에 기침이 심할 경우 진해제를 복용해 숙면 도움"
    }
}

# 증상 선택
symptom = st.selectbox("💡 증상을 선택하세요", [""] + list(medicine_dict.keys()))

# 💊 이모지 표시용 자리
emoji_slot = st.empty()

# 추천 결과 출력
if symptom:
    # 잠깐 💊 애니메이션 표시
    emoji_slot.markdown("<p class='emoji'>💊</p>", unsafe_allow_html=True)
    time.sleep(0.5)  # 0.5초 후 사라지게
    emoji_slot.empty()
    
    info = medicine_dict[symptom]
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"<h2 class='highlight'>{symptom}</h2>", unsafe_allow_html=True)
    st.markdown(f"💊 추천 약: **{info['약']}**")
    st.markdown(f"⚠️ 예상 부작용: **{info['부작용']}**")
    st.markdown(f"📝 생활 관리법: **{info['관리법']}**")
    st.markdown(f"🕒 복용 시간: **{info['복용시간']}**")
    st.markdown(f"⚠️ 주의사항: **{info['주의사항']}**")
    st.markdown(f"💡 복용 팁: **{info['복용팁']}**")
    st.markdown("</div>", unsafe_allow_html=True)
