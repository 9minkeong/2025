import streamlit as st

# ----------------------
# 기본 설정
# ----------------------
st.set_page_config(page_title="헌터헌터 인물 백과사전", page_icon="🪄", layout="wide")
st.title("✨ 헌터헌터 인물 백과사전 🪄")

st.sidebar.title("등장인물 선택")

# ----------------------
# 데이터: 인물 + 이미지 + 설명
# ----------------------
characters = {
    "곤 프릭스": {
        "img": "https://static.wikia.nocookie.net/hunterxhunter/images/2/28/Gon2011.png",  # 헌터헌터 위키 이미지 주소 예시
        "desc": "주인공. 호기심 많고 순수한 소년으로, 아버지 진을 찾기 위해 헌터가 된다. 주 능력은 '자넨(자연 에너지)'을 활용한 '자넨주권' 공격.",
        "ability": "⚡ 자넨 / 장점: 무한한 잠재력"
    },
    "킬루아 조르딕": {
        "img": "https://static.wikia.nocookie.net/hunterxhunter/images/6/65/Killua2011.png",
        "desc": "곤의 절친이자 암살자 가문 출신. 전기 계열 능력을 자유자재로 다룬다.",
        "ability": "⚡ 번개 능력 / 장점: 스피드와 전격"
    },
    "쿠라피카": {
        "img": "https://static.wikia.nocookie.net/hunterxhunter/images/8/8a/Kurapika2011.png",
        "desc": "쿠르타족의 마지막 생존자. 붉은 눈을 되찾기 위해 복수를 다짐한다.",
        "ability": "🔗 체인 능력 / 장점: 강한 복수심과 전략"
    },
    "레오리오": {
        "img": "https://static.wikia.nocookie.net/hunterxhunter/images/d/d4/Leorio2011.png",
        "desc": "의사가 되기 위해 헌터가 된 인물. 정의감이 강하고 동료애가 깊다.",
        "ability": "💉 의료 지식 + 네넨 응용"
    },
    "히소카": {
        "img": "https://static.wikia.nocookie.net/hunterxhunter/images/4/45/Hisoka2011.png",
        "desc": "광기 어린 마술사. 강한 상대와의 전투를 즐기며 예측불가한 존재.",
        "ability": "🎭 바지컬 고무 / 장점: 교활함과 창의성"
    }
}

# ----------------------
# UI: 캐릭터 선택
# ----------------------
choice = st.sidebar.radio("등장인물을 선택하세요:", list(characters.keys()))

char = characters[choice]

col1, col2 = st.columns([1,2])
with col1:
    st.image(char["img"], caption=choice, use_column_width=True)
with col2:
    st.subheader(choice)
    st.write(char["desc"])
    st.success(char["ability"])

st.markdown("---")
st.caption("출처: Hunter x Hunter Wiki (공식 이미지 URL 사용)")
