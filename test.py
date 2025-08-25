import streamlit as st
import time

# ── 페이지 & 스타일 ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="💊 증상별 약 추천 (스텝형)", page_icon="💊", layout="wide")
st.markdown("""
<style>
.stApp { background-color:#F0F8FF; }
.title { color:#4B0082; text-align:center; margin-top:4px; }
.step { background:#ffffff; border-radius:14px; padding:18px 20px; box-shadow:2px 2px 14px rgba(0,0,0,0.08); margin: 8px 0 18px; }
.card { background:#ffffff; border-radius:14px; padding:18px 20px; box-shadow:2px 2px 14px rgba(0,0,0,0.08); }
.highlight { color:#FF4500; font-weight:700; }
.hr { height:1px; background:linear-gradient(90deg,#fff, #c8c8ff, #fff); border:0; margin:14px 0; }
.emoji { font-size:48px; text-align:center; animation: pop .5s ease-in-out; }
@keyframes pop { 0%{transform:scale(0);} 50%{transform:scale(1.5);} 100%{transform:scale(1);} }
.small { color:#555; font-size:0.92rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='title'>💊 증상별 약 추천 · 스텝형 선택</h1>", unsafe_allow_html=True)
st.write("⚠️ 이 앱은 **의료 참고용**입니다. 정확한 진단/처방은 반드시 **의사·약사**에게 받으세요.")

# ── 데이터 ──────────────────────────────────────────────────────────────────────
DB = {
    "두통": {
        "약": "진통제 (예: 타이레놀, 이부프로펜)",
        "부작용": "속쓰림, 위장 장애, 드물게 간 기능 문제",
        "관리법": "수분 섭취, 눈 휴식, 규칙적 수면, 스트레스 관리",
        "복용시간": "증상 발생 시, 하루 최대 4회",
        "주의사항": "간 질환 병력 있으면 복용 전 상담",
        "복용팁": "가능하면 식후 복용해 위장 부담 감소"
    },
    "발열": {
        "약": "해열제 (예: 아세트아미노펜, 이부프로펜)",
        "부작용": "간 손상(과량), 위장 장애, 드물게 알레르기",
        "관리법": "수분 보충, 가벼운 복장, 휴식, 체온 모니터링",
        "복용시간": "6~8시간 간격 필요 시 복용",
        "주의사항": "어린이/노인/간 질환자 주의",
        "복용팁": "하루 최대 용량 준수, 38℃ 이상일 때 필요 시 사용"
    },
    "기침": {
        "약": "진해제·거담제 (예: 덱스트로메토르판, 암브록솔)",
        "부작용": "졸림, 어지럼, 장기 사용 시 의존 우려",
        "관리법": "따뜻한 음료, 가습, 충분한 휴식",
        "복용시간": "하루 2~3회 필요 시",
        "주의사항": "만 2세 이하 사용 제한",
        "복용팁": "야간 기침 심하면 취침 전 진해제"
    },
    "속쓰림": {
        "약": "제산제·PPI (예: 오메프라졸)",
        "부작용": "설사·변비, 장기 사용 시 영양 흡수 저하",
        "관리법": "카페인·기름진 음식 피하기, 식후 바로 눕지 않기",
        "복용시간": "식전 30분 또는 취침 전",
        "주의사항": "장기 복용 전 상담 권장",
        "복용팁": "증상 심하면 1일 2회 분복 고려(의사 지시 우선)"
    },
    "근육통": {
        "약": "진통·소염제 (예: 이부프로펜, 나프록센), 파스",
        "부작용": "위장 장애, 피부 자극, 드물게 신장 영향",
        "관리법": "스트레칭, 온찜질, 휴식, 과사용 방지",
        "복용시간": "증상 시 1일 최대 3~4회",
        "주의사항": "신장/위장 질환자 주의",
        "복용팁": "단기 집중 사용, 장기 연속 복용은 피하기"
    }
}

# ── 상태 ───────────────────────────────────────────────────────────────────────
if "results" not in st.session_state:
    st.session_state.results = []

# ── 스텝 1: 증상 선택 ──────────────────────────────────────────────────────────
with st.container():
    st.markdown("<div class='step'>", unsafe_allow_html=True)
    st.subheader("① 증상 선택")
    col_s1, col_s2 = st.columns([2,1])
    with col_s1:
        symptom = st.selectbox("증상을 하나 선택하세요", [""] + list(DB.keys()), index=0)
    with col_s2:
        st.markdown("<p class='small'>증상은 한 번에 하나씩 추가됩니다. 여러 증상을 비교하려면 아래에서 반복해 **추가하기**를 눌러 주세요.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ── 스텝 2: 표시할 항목 고르기(하나하나 체크) ────────────────────────────────────
with st.container():
    st.markdown("<div class='step'>", unsafe_allow_html=True)
    st.subheader("② 표시할 정보 고르기 (원하는 것만 체크)")
    c1, c2, c3 = st.columns(3)
    with c1:
        f_drug = st.checkbox("💊 약", value=True)
        f_side = st.checkbox("⚠️ 부작용", value=True)
    with c2:
        f_care = st.checkbox("📝 생활 관리법", value=True)
        f_time = st.checkbox("🕒 복용 시간", value=True)
    with c3:
        f_warn = st.checkbox("❗ 주의사항", value=True)
        f_tip  = st.checkbox("💡 복용 팁", value=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ── 스텝 3: 추가하기(💊 팝 애니메이션) ───────────────────────────────────────────
emoji_slot = st.empty()
st.markdown("<hr class='hr'/>", unsafe_allow_html=True)
col_add, col_clear = st.columns([1,1])

with col_add:
    if st.button("➕ 선택 내용 카드로 추가하기", use_container_width=True):
        if not symptom:
            st.warning("증상을 먼저 선택하세요.")
        elif not any([f_drug, f_side, f_care, f_time, f_warn, f_tip]):
            st.warning("표시할 항목을 최소 1개 이상 선택하세요.")
        else:
            # 💊 팝
            emoji_slot.markdown("<div class='emoji'>💊</div>", unsafe_allow_html=True)
            time.sleep(0.5)
            emoji_slot.empty()

            item = {"증상": symptom, "표시": []}
            if f_drug: item["표시"].append(("💊 추천 약", DB[symptom]["약"]))
            if f_side: item["표시"].append(("⚠️ 부작용", DB[symptom]["부작용"]))
            if f_care: item["표시"].append(("📝 생활 관리법", DB[symptom]["관리법"]))
            if f_time: item["표시"].append(("🕒 복용 시간", DB[symptom]["복용시간"]))
            if f_warn: item["표시"].append(("❗ 주의사항", DB[symptom]["주의사항"]))
            if f_tip:  item["표시"].append(("💡 복용 팁", DB[symptom]["복용팁"]))
            st.session_state.results.append(item)
            st.success(f"'{symptom}' 카드가 추가되었습니다!")

with col_clear:
    if st.button("🗑️ 전체 카드 지우기", use_container_width=True, type="secondary"):
        st.session_state.results.clear()
        st.info("모든 카드가 삭제되었습니다.")

# ── 선택된 카드 목록 ────────────────────────────────────────────────────────────
st.markdown("### 📋 선택된 카드")
if not st.session_state.results:
    st.write("아직 추가된 카드가 없습니다. 위에서 증상과 항목을 선택한 뒤 **➕ 추가하기**를 눌러 보세요.")
else:
    for idx, item in enumerate(st.session_state.results):
        with st.container():
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            top = st.columns([5,1])
            with top[0]:
                st.markdown(f"#### <span class='highlight'>{item['증상']}</span>", unsafe_allow_html=True)
            with top[1]:
                if st.button("삭제", key=f"del_{idx}"):
                    del st.session_state.results[idx]
                    st.experimental_rerun()

            st.markdown("<hr class='hr'/>", unsafe_allow_html=True)
            for label, value in item["표시"]:
                st.markdown(f"**{label}**: {value}")
            st.markdown("</div>", unsafe_allow_html=True)
