import streamlit as st

# 페이지 설정
st.set_page_config(page_title="💊 증상별 약 추천", page_icon="💊", layout="wide")

# CSS 스타일링
st.markdown("""
    <style>
    /* 전체 배경색 */
    .stApp {
        background-color: #F0F8FF;
    }
    /* 카드 느낌 박스 */
    .card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 3px 3px 20px rgba(0,0,0,0.1);
        margin-bottom: 25px;
    }
    /* 제목 스타일 */
    .title {
        color: #4B0082;
        text-align: center;
    }
    /* 강조 텍스트 */
    .highlight {
        color: #FF4500;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# 상단 제목
st.markdown("<h1 class='title'>💊 증상별 약 추천 & 관리법</h1>", unsafe_allow_html=True)
st.write("⚠️ 이 앱은 의료 참고용입니다. 정확한 진단은 반드시 의사·약사에게 받으세요.")

# 데이터베이스 확장
medicine_dict = {
    "두통": {
        "약": "진통제 (예: 타이레놀, 이부프로펜)",
        "부작용": "속쓰림, 위장 장애, 드물게 간 기능 문제",
        "관리법": "충분한 수분 섭취, 눈 휴식, 규칙적인 수면, 스트레스 관리",
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
    },
    "속쓰림": {
        "약": "제산제, 위산 억제제 (예: 라니티딘, 오메프라졸)",
        "부작용": "설사, 변비, 장기 복용 시 영양 흡수 감소",
        "관리법": "카페인, 기름진 음식 피하기, 식사 후 바로 눕지 않기, 규칙적 식사",
        "복용시간": "식사 30분 전 또는 저녁 취침 전",
        "주의사항": "장기간 사용 시 의사 상담 필요",
        "복용팁": "증상이 심한 경우 하루 2회로 나누어 복용 가능"
    },
    "근육통": {
        "약": "진통·소염제 (예: 이부프로펜, 나프록센), 파스",
        "부작용": "위장 장애, 피부 자극, 드물게 신장 영향",
        "관리법": "적절한 스트레칭, 온찜질 또는 휴식, 과사용 방지",
        "복용시간": "증상 발생 시, 하루 최대 3~4회",
        "주의사항": "신장 질환, 위장 질환 있는 경우 주의",
        "복용팁": "통증이 심할 때 단기 집중 사용, 장기 사용 피하기"
    }
}

# 증상 선택
symptom = st.selectbox("💡 증상을 선택하세요", [""] + list(medicine_dict.keys()))

# 추천 결과 출력
if symptom:
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
