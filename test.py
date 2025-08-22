import streamlit as st

# 페이지 설정
st.set_page_config(page_title="💊 증상별 약 추천", page_icon="💊", layout="wide")

st.markdown("<h1 style='text-align:center; color:#4B0082;'>💊 증상별 약 추천 & 관리법</h1>", unsafe_allow_html=True)
st.write("⚠️ 이 앱은 의료 참고용입니다. 정확한 진단은 반드시 의사·약사에게 받으세요.")

# 증상-약-부작용-관리법-복용시간-이미지 데이터
medicine_dict = {
    "두통": {
        "약": "진통제 (예: 타이레놀, 이부프로펜)",
        "부작용": "속쓰림, 위장 장애",
        "관리법": "충분한 수분 섭취, 눈 휴식, 규칙적인 수면",
        "복용시간": "증상 발생 시, 하루 최대 4회",
        "이미지": "https://upload.wikimedia.org/wikipedia/commons/5/5c/Paracetamol_500mg_pills.jpg"
    },
    "발열": {
        "약": "해열제 (예: 아세트아미노펜, 이부프로펜)",
        "부작용": "간 손상(과량 복용 시), 위장 장애",
        "관리법": "충분한 수분 섭취, 가벼운 옷 착용, 휴식",
        "복용시간": "6~8시간 간격으로 필요 시 복용",
        "이미지": "https://upload.wikimedia.org/wikipedia/commons/d/d9/Ibuprofen_pills.jpg"
    },
    "기침": {
        "약": "진해제, 거담제 (예: 덱스트로메토르판, 암브록솔)",
        "부작용": "졸림, 어지럼증",
        "관리법": "따뜻한 음료 섭취, 실내 습도 유지",
        "복용시간": "하루 2~3회, 필요 시 복용",
        "이미지": "https://upload.wikimedia.org/wikipedia/commons/0/0b/Cough_syrup.jpg"
    },
    "속쓰림": {
        "약": "제산제, 위산 억제제 (예: 라니티딘, 오메프라졸)",
        "부작용": "설사, 변비",
        "관리법": "카페인, 기름진 음식 피하기, 식사 후 바로 눕지 않기",
        "복용시간": "식사 30분 전 또는 저녁 취침 전",
        "이미지": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Omeprazole_drug.jpg"
    },
    "근육통": {
        "약": "진통·소염제 (예: 이부프로펜, 나프록센), 파스",
        "부작용": "위장 장애, 피부 자극",
        "관리법": "적절한 스트레칭, 온찜질 또는 휴식",
        "복용시간": "증상 발생 시, 하루 최대 3~4회",
        "이미지": "https://upload.wikimedia.org/wikipedia/commons/f/fb/Naproxen_tablets.jpg"
    }
}

# 선택 박스
symptom = st.selectbox("💡 증상을 선택하세요", [""] + list(medicine_dict.keys()))

# 결과 출력
if symptom:
    info = medicine_dict[symptom]
    
    # 2열 레이아웃: 왼쪽 이미지, 오른쪽 텍스트
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image(info['이미지'], use_column_width=True)
        
    with col2:
        st.markdown(f"<h2 style='color:#4B0082;'>{symptom}</h2>", unsafe_allow_html=True)
        st.markdown(f"**💊 추천 약:** {info['약']}")
        st.markdown(f"**⚠️ 예상 부작용:** {info['부작용']}")
        st.markdown(f"**📝 생활 관리법:** {info['관리법']}")
        st.markdown(f"**🕒 복용 시간:** {info['복용시간']}")
    
    st.markdown("---")
