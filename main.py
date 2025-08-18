import streamlit as st
import pandas as pd

# ----------------------
# Hunter x Hunter — 인물 백과사전 (Streamlit)
# 파일명: hunter_hunter_encyclopedia.py
# ----------------------

st.set_page_config(page_title="헌터 x 헌터 — 인물 백과사전", page_icon="🪄", layout="wide")

# --- 스타일 ---
st.markdown(r"""
<style>
body { background: linear-gradient(120deg,#0f172a 0%, #1f2937 50%); color: #f8fafc }
h1 { font-weight: 800; font-size: 2.2rem; letter-spacing: 0.6px }
.card { background: rgba(255,255,255,0.03); border-radius: 12px; padding: 14px; border: 1px solid rgba(255,255,255,0.04); }
.small { font-size:0.9rem; color: #e6eef8 }
.key { color:#ffd166; font-weight:700 }
img { border-radius: 8px }
</style>
""", unsafe_allow_html=True)

st.title("✨ 헌터 × 헌터 — 인물 백과사전 🪄")
st.write("간단한 인물 정보, 능력(넨), 속성, 대표 이미지까지 한 곳에 정리해 보여줍니다. 교육/참고용으로 사용하세요.")

# ----------------------
# 인물 데이터 (이미지 URL 포함)
# 주의: 이미지 URL은 공개 호스팅된 자원을 사용합니다(예: 팬 위키). 저작권에 유의하세요.
# ----------------------
characters = {
    "Gon Freecss (곤 프릭스)": {
        "img": "https://static.wikia.nocookie.net/hunterxhunter/images/2/28/Gon2011.png",
        "bio": "본 작품의 주인공. 밝고 호기심 많으며 우정에 대한 충성심이 강하다. 아버지 '진'을 찾아 헌터가 되려 한다.",
        "nen_type": "변형(변화)/최적화(강화) — 자넨(Jajanken): 바위/가위/보 형태의 공격 기술",
        "affiliation": "본인(로컬 헌터) / 주요 동료: 킬루아, 쿠라피카, 레오리오",
        "first_appearance": "만화 초반 — 헌터 시험 편",
        "seiyuu": "중요 성우(일본어): 히라노 아야(초기) 등",
        "notable_techniques": ["자넨 - Rock (강화형, 근접 파워)", "자넨 - Scissors (근접/절단)", "자넨 - Paper (원거리/기술)"] ,
        "personality": "순수, 결단력, 강한 정의감",
        "stats": {"힘":8, "속도":8, "지능":6, "넨 제어":7}
    },
    "Killua Zoldyck (킬루아 조르딕)": {
        "img": "https://static.wikia.nocookie.net/hunterxhunter/images/6/65/Killua2011.png",
        "bio": "명문 암살자 가문 조르딕 출신. 어린 시절부터 암살 훈련을 받아 치명적인 전투 능력을 지님. 곤의 절친이자 우정의 화신.",
        "nen_type": "발전(변화) 계열, 전격(번개) 특화",
        "affiliation": "조르딕 가문(과거) / 곤 일행",
        "first_appearance": "헌터 시험 편",
        "seiyuu": "중요 성우(일본어): 사토 리나 (성우 변동 가능)",
        "notable_techniques": ["전격(번개) 기반 기술들", "암살술, 스피드/민첩성 극강"],
        "personality": "장난기 많음과 냉철함이 공존, 친구에게 헌신적",
        "stats": {"힘":7, "속도":10, "지능":8, "넨 제어":8}
    },
    "Kurapika (쿠라피카)": {
        "img": "https://static.wikia.nocookie.net/hunterxhunter/images/8/8a/Kurapika2011.png",
        "bio": "쿠르타족의 마지막 생존자. 부족의 붉은 눈을 되찾고자 복수를 결심한 인물로, 목적을 위해 강한 의지를 보인다.",
        "nen_type": "조정(조종)/강화 특화 — 사슬(체인)을 이용한 전용기 발동",
        "affiliation": "블랙리스트 헌터, 필요시 조직과 연대",
        "first_appearance": "헌터 시험 편 - 초기 에피소드",
        "seiyuu": "중요 성우(일본어): 하야미 사오리(예시)",
        "notable_techniques": ["체인 관련 전용기: 천벌의 사슬 등", "특수 전투 전술"],
        "personality": "냉정, 치밀, 복수심이 행동 동기",
        "stats": {"힘":7, "속도":7, "지능":9, "넨 제어":9}
    },
    "Leorio (레오리오 파라디나이트)": {
        "img": "https://static.wikia.nocookie.net/hunterxhunter/images/d/d4/Leorio2011.png",
        "bio": "의사가 되기 위해 헌터가 된 인물. 외형적으로는 다소 거칠어 보이지만 동료애가 강하고 정의감이 있다.",
        "nen_type": "주로 보조·실무형 넨 활용(의료/방어 중심)",
        "affiliation": "곤 일행 / 의료 지향",
        "first_appearance": "헌터 시험 편",
        "seiyuu": "중요 성우(일본어): 사토 타케루(예시)",
        "notable_techniques": ["의료 지식 응용, 원거리 타격(후기 설정)", "대인 지원 능력"],
        "personality": "다정하고 현실적인 면이 있음, 친구 위해 적극적",
        "stats": {"힘":6, "속도":5, "지능":7, "넨 제어":6}
    },
    "Hisoka (히소카 모로우)": {
        "img": "https://static.wikia.nocookie.net/hunterxhunter/images/4/45/Hisoka2011.png",
        "bio": "광기와 예술적 성향이 결합된 전투광. 강한 상대를 찾아 싸우는 것을 즐긴다. 예측불가한 행동과 전략을 보여준다.",
        "nen_type": "변화(텍스처 서프라이즈) / 접착(번지검 - Bungee Gum) 등 독창적 기술",
        "affiliation": "프로 헌터(필요시 현상금 사냥 등)",
        "first_appearance": "헌터 시험 편 — 초기 대립 캐릭터",
        "seiyuu": "중요 성우(일본어): 히카루 미츠루(예시)",
        "notable_techniques": ["번지검(Bungee Gum)", "텍스처 서프라이즈(Texture Surprise)"],
        "personality": "도발적이고 잔혹하지만, 전투에 대한 미학을 가짐",
        "stats": {"힘":9, "속도":8, "지능":9, "넨 제어":9}
    }
}

# ----------------------
# 인터페이스
# ----------------------
st.sidebar.header("🔎 검색 & 선택")
names = list(characters.keys())
selected = st.sidebar.selectbox("인물 선택", names, index=0)
query = st.sidebar.text_input("이름/키워드 검색 (빈칸 허용)")

# 검색 기능 (간단)
if query:
    hits = [n for n in names if query.lower() in n.lower() or any(query.lower() in str(v).lower() for v in characters[n].values())]
    if hits:
        selected = st.sidebar.selectbox("검색 결과", hits)
    else:
        st.sidebar.warning("검색 결과가 없습니다.")

char = characters[selected]

col1, col2 = st.columns([1,2])
with col1:
    st.image(char['img'], use_column_width=True, caption=selected)
    st.markdown(f"<div class='card small'><b class='key'>넨 유형</b>: {char['nen_type']}<br><b class='key'>소속</b>: {char['affiliation']}<br><b class='key'>첫등장</b>: {char['first_appearance']}</div>", unsafe_allow_html=True)
    st.markdown("
")
    if st.button("⭐ 즐겨찾기 추가"):
        if 'favs' not in st.session_state:
            st.session_state['favs'] = []
        if selected not in st.session_state['favs']:
            st.session_state['favs'].append(selected)
            st.success("즐겨찾기에 추가되었습니다!")

with col2:
    st.header(selected)
    st.write(char['bio'])
    st.subheader("주요 스킬 / 기술")
    for t in char['notable_techniques']:
        st.markdown(f"- {t}")
    st.subheader("성격 및 메모")
    st.write(char['personality'])

    st.subheader("스탯(참고용)")
    stats = pd.DataFrame.from_dict(char['stats'], orient='index', columns=['수치']).reset_index()
    stats.columns = ['능력', '수치']
    st.table(stats)

    with st.expander("더 자세한 정보 보기 (성우, 출처 등)"):
        st.markdown(f"- 성우(일본어, 예시): {char.get('seiyuu','-')}
- 원본 이미지/세부 출처: 팬 위키(Hunterpedia / Fandom) 혹은 공식 자료 참고 권장")

# 즐겨찾기 표시
st.markdown("---")
if 'favs' in st.session_state and st.session_state['favs']:
    st.subheader("⭐ 나의 즐겨찾기")
    for f in st.session_state['favs']:
        st.markdown(f"- {f}")

# 전체 테이블
st.markdown("---")
st.subheader("📚 전체 인물 목록 (요약)")
summary_rows = []
for name, v in characters.items():
    summary_rows.append({
        '이름': name,
        '넨 유형': v['nen_type'],
        '소속': v['affiliation']
    })
summary_df = pd.DataFrame(summary_rows)
st.dataframe(summary_df, use_container_width=True)

# CSV 다운로드
csv = summary_df.to_csv(index=False).encode('utf-8-sig')
st.download_button("📥 전체 인물 CSV로 저장", data=csv, file_name="hxh_characters.csv", mime="text/csv")

st.caption("참고: 이 앱은 팬용 비공식 백과사전 예시입니다. 이미지와 상세 설정은 팬 위키/공식 자료를 출처로 참고하세요.")
