import streamlit as st
import pandas as pd
from datetime import datetime

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="MBTI 진로 추천 🎯", 
    page_icon="🎪", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# -------------------- CUSTOM STYLES --------------------
st.markdown(
    r"""
    <style>
    /* Page background */
    .stApp {
        background: linear-gradient(120deg, #1b1f3a 0%, #41295a 40%, #2F0743 60%, #0f2027 100%);
        color: #f7f7ff;
    }
    /* Fancy gradient header text */
    .gradient-text {
        font-weight: 800;
        background: linear-gradient(90deg, #ffdd00, #ff7a00, #ff00aa, #7afff5, #00e1ff);
        -webkit-background-clip: text; background-clip: text; color: transparent;
        text-shadow: 0 0 18px rgba(255,255,255,0.15);
        letter-spacing: 0.5px;
    }
    .subtle {
        opacity: 0.95;
    }
    /* Cards */
    .card {
        border-radius: 18px; padding: 18px 18px; margin-bottom: 16px;
        background: rgba(255,255,255,0.06); backdrop-filter: blur(6px);
        border: 1px solid rgba(255,255,255,0.12);
        box-shadow: 0 10px 24px rgba(0,0,0,0.25);
    }
    .badge {
        display: inline-block; padding: 4px 10px; border-radius: 999px; margin: 4px 6px 0 0;
        background: linear-gradient(135deg, rgba(255,255,255,0.12), rgba(255,255,255,0.06));
        border: 1px solid rgba(255,255,255,0.2); font-size: 0.78rem;
    }
    .tiny { font-size: 0.82rem; opacity: 0.9; }

    /* Emoji rain */
    .emoji-rain { position: fixed; left: 0; top: 0; width: 100%; height: 0; pointer-events: none; z-index: 9999; }
    .emoji { position: absolute; top: -2rem; font-size: 1.6rem; animation: fall 6s linear forwards; filter: drop-shadow(0 6px 8px rgba(0,0,0,0.4));}
    @keyframes fall { to { transform: translateY(150vh) rotate(360deg);} }

    /* Tables */
    .stDataFrame { border-radius: 16px; overflow: hidden; }

    /* Sidebar polish */
    section[data-testid="stSidebar"] > div { background: rgba(0,0,0,0.35); }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------- FUN: EMOJI RAIN (on first load) ---------------
import random
emojis = list("💼🧠✨🎨🧪🛠️🛰️⚙️📚🧬💡🧯🧭🧱📈💻🎧🎓🏥🧰🌏🚀📸🎭🎮🧩🤝🎯")
if 'rained' not in st.session_state:
    st.session_state['rained'] = True
    drops = ''.join([
        f'<span class="emoji" style="left:{random.randint(0,100)}%; animation-delay:{random.random()*2:.2f}s">{random.choice(emojis)}</span>'
        for _ in range(60)
    ])
    st.markdown(f'<div class="emoji-rain">{drops}</div>', unsafe_allow_html=True)

# -------------------- HEADER --------------------
col1, col2 = st.columns([0.85, 0.15])
with col1:
    st.markdown("""
    <h1 class="gradient-text">🎪 MBTI Career Carnival — 나만의 진로 🎯</h1>
    <div class="subtle">성향 × 흥미 × 강점으로 ✨반짝이는✨ 직업 추천을 받아보세요!</div>
    """, unsafe_allow_html=True)
with col2:
    st.metric(label="오늘 날짜", value=datetime.now().strftime("%Y-%m-%d"), delta="행복 지수 ☀️")

st.divider()

# -------------------- DATA --------------------
# MBTI -> base career affinity (Korean)
mbti_clusters = {
    'Analysts 🧠': ["INTJ", "INTP", "ENTJ", "ENTP"],
    'Diplomats 🤝': ["INFJ", "INFP", "ENFJ", "ENFP"],
    'Sentinels 🛡️': ["ISTJ", "ISFJ", "ESTJ", "ESFJ"],
    'Explorers 🧭': ["ISTP", "ISFP", "ESTP", "ESFP"],
}

careers = [
    {"name":"데이터 사이언티스트", "emoji":"📊", "tags":["STEM","Tech","Problem-Solving"], "fit":{"Analysts 🧠":9, "Sentinels 🛡️":7}, "styles":{"solo":1, "team":1}},
    {"name":"소프트웨어 엔지니어", "emoji":"💻", "tags":["STEM","Tech","Maker"], "fit":{"Analysts 🧠":9, "Explorers 🧭":8}, "styles":{"solo":1,"team":1}},
    {"name":"프로덕트 매니저", "emoji":"🧭", "tags":["Business","Tech","Leadership"], "fit":{"Analysts 🧠":8, "Diplomats 🤝":8, "Sentinels 🛡️":7}, "styles":{"team":2}},
    {"name":"연구원(바이오/과학)", "emoji":"🧪", "tags":["STEM","Science","Health"], "fit":{"Analysts 🧠":9, "Diplomats 🤝":7}, "styles":{"solo":2}},
    {"name":"약사", "emoji":"💊", "tags":["Health","Precision","Education"], "fit":{"Sentinels 🛡️":9, "Diplomats 🤝":8}, "styles":{"team":1}},
    {"name":"간호사", "emoji":"🏥", "tags":["Health","Care","Teamwork"], "fit":{"Diplomats 🤝":8, "Sentinels 🛡️":8}, "styles":{"team":2}},
    {"name":"교사", "emoji":"🎓", "tags":["Education","Care","Communication"], "fit":{"Diplomats 🤝":9, "Sentinels 🛡️":8}, "styles":{"team":1}},
    {"name":"UX/UI 디자이너", "emoji":"🎨", "tags":["Design","Tech","Creativity"], "fit":{"Diplomats 🤝":8, "Explorers 🧭":8}, "styles":{"team":1}},
    {"name":"마케팅 전략가", "emoji":"📣", "tags":["Business","Creativity","Communication"], "fit":{"Diplomats 🤝":8, "Explorers 🧭":7}, "styles":{"team":2}},
    {"name":"재무/회계", "emoji":"🧮", "tags":["Business","Precision","Stability"], "fit":{"Sentinels 🛡️":9}, "styles":{"solo":1}},
    {"name":"프로덕트 디자이너", "emoji":"🧰", "tags":["Design","Maker","Creativity"], "fit":{"Explorers 🧭":9, "Diplomats 🤝":7}, "styles":{"team":1}},
    {"name":"데브옵스/클라우드 엔지니어", "emoji":"🛰️", "tags":["STEM","Tech","Ops"], "fit":{"Analysts 🧠":8, "Sentinels 🛡️":8}, "styles":{"team":1}},
    {"name":"품질관리(QA)", "emoji":"🧪", "tags":["Precision","Manufacturing","Stability"], "fit":{"Sentinels 🛡️":9}, "styles":{"solo":1}},
    {"name":"세일즈/BD", "emoji":"🤝", "tags":["Business","Communication","Outdoors"], "fit":{"Explorers 🧭":9, "Diplomats 🤝":8}, "styles":{"team":2}},
    {"name":"콘텐츠 크리에이터", "emoji":"🎬", "tags":["Creativity","Media","Independence"], "fit":{"Explorers 🧭":8, "Diplomats 🤝":8}, "styles":{"solo":1}},
    {"name":"산업디자이너", "emoji":"🛠️", "tags":["Design","Maker","Manufacturing"], "fit":{"Explorers 🧭":9}, "styles":{"team":1}},
    {"name":"사회복지사", "emoji":"🫶", "tags":["Care","Social Impact","Communication"], "fit":{"Diplomats 🤝":9}, "styles":{"team":2}},
    {"name":"공무원/행정", "emoji":"🏛️", "tags":["Stability","Service","Organization"], "fit":{"Sentinels 🛡️":9}, "styles":{"team":1}},
    {"name":"파일럿/드론 운영", "emoji":"✈️", "tags":["Tech","Outdoors","Precision"], "fit":{"Explorers 🧭":8, "Analysts 🧠":7}, "styles":{"team":1}},
    {"name":"환경공학자", "emoji":"🌿", "tags":["STEM","Sustainability","Fieldwork"], "fit":{"Analysts 🧠":8, "Explorers 🧭":8}, "styles":{"team":1}},
]

career_df = pd.DataFrame(careers)

# -------------------- INPUTS (SIDEBAR) --------------------
st.sidebar.title("🎛️ 설정 & 취향 믹서")
mbti_list = sum(mbti_clusters.values(), [])
mbti = st.sidebar.selectbox("👉 나의 MBTI", options=mbti_list, index=mbti_list.index("INTJ") if "INTJ" in mbti_list else 0)

strengths = st.sidebar.multiselect(
    "💪 강점(복수 선택)",
    ["논리적 사고", "창의성", "공감", "리더십", "손기술", "문제해결", "커뮤니케이션", "꼼꼼함", "기획력", "디자인 감각"],
    default=["문제해결", "창의성"]
)

interests = st.sidebar.multiselect(
    "🎯 관심 분야",
    ["STEM", "Tech", "Design", "Business", "Health", "Education", "Creativity", "Manufacturing", "Social Impact", "Outdoors", "Stability", "Precision"],
    default=["STEM", "Tech", "Design"]
)

work_mode = st.sidebar.radio("🧑‍🤝‍🧑 선호 작업 형태", ["혼자 몰입", "팀 협업", "상관 없음"], index=1)
need_stability = st.sidebar.slider("🧱 안정성 선호 (낮음→높음)", 0, 10, 6)
need_outdoor = st.sidebar.slider("🌤️ 야외 활동 선호 (실내→야외)", 0, 10, 4)

if st.sidebar.button("🎆 추천 받기!", type="primary"):
    st.balloons()
    st.toast("반짝반짝! 추천을 새로 만들었어요 ✨", icon="✨")

# -------------------- SCORING --------------------
cluster_of_mbti = next((cluster for cluster, types in mbti_clusters.items() if mbti in types), None)

weights = {
    'base_fit': 5.0,      # MBTI 클러스터 적합도 가중치
    'interest': 1.5,      # 관심 태그 가중치
    'strengths': 1.0,     # 강점 보너스 (간접 반영)
    'stability': 0.6,
    'outdoor': 0.6,
    'style': 1.4,
}

strength_map = {
    "논리적 사고":["STEM","Problem-Solving","Precision"],
    "창의성":["Creativity","Design","Media"],
    "공감":["Care","Communication","Education"],
    "리더십":["Leadership","Business"],
    "손기술":["Maker","Manufacturing"],
    "문제해결":["Problem-Solving","STEM"],
    "커뮤니케이션":["Communication","Business"],
    "꼼꼼함":["Precision","Stability"],
    "기획력":["Business","Leadership"],
    "디자인 감각":["Design","Creativity"],
}

# soft tag set from strengths
strength_tags = set(tag for s in strengths for tag in strength_map.get(s, []))

scored = []
for _, row in career_df.iterrows():
    base = row['fit'].get(cluster_of_mbti, 6)
    score = base * weights['base_fit']

    # interest overlap
    overlap = len(set(row['tags']) & set(interests))
    score += overlap * 2 * weights['interest']

    # strength-tag boosting
    s_overlap = len(set(row['tags']) & strength_tags)
    score += s_overlap * 1.5 * weights['strengths']

    # stability preference
    if "Stability" in row['tags']:
        score += need_stability * weights['stability'] * 0.6
    else:
        score += max(0, (5 - abs(need_stability-5))) * weights['stability'] * 0.2

    # outdoor preference (heuristic)
    if "Outdoors" in row['tags'] or "Fieldwork" in row['tags']:
        score += need_outdoor * weights['outdoor'] * 0.5
    else:
        score += (10-need_outdoor) * weights['outdoor'] * 0.2

    # work style
    if work_mode == "혼자 몰입":
        style_bonus = row['styles'].get('solo', 0) * 2.0
    elif work_mode == "팀 협업":
        style_bonus = row['styles'].get('team', 0) * 2.0
    else:
        style_bonus = max(row['styles'].values()) if row['styles'] else 0
    score += style_bonus * weights['style']

    scored.append({
        '직업': f"{row['emoji']} {row['name']}",
        '점수': round(score, 2),
        '태그': ", ".join(row['tags'])
    })

result_df = pd.DataFrame(scored).sort_values('점수', ascending=False).reset_index(drop=True)

# -------------------- LAYOUT --------------------
res_tab, encyclopedia_tab, roadmap_tab = st.tabs(["💥 추천 결과", "📚 직업 백과", "🗺️ 로드맵"])

with res_tab:
    st.subheader("💥 나에게 딱! TOP 추천")
    top_n = 8
    top_df = result_df.head(top_n)

    # Show colorful cards
    rows = (top_n + 3)//4
    idx = 0
    for r in range(rows):
        cols = st.columns(4)
        for c in cols:
            if idx >= len(top_df):
                break
            row = top_df.iloc[idx]
            title = row['직업']
            tags = row['태그'].split(", ")
            with c:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown(f"<h3 class='gradient-text' style='font-size:1.1rem'>{title}  ✨</h3>", unsafe_allow_html=True)
                st.markdown(f"<div class='tiny'>점수: <b>{row['점수']}</b></div>", unsafe_allow_html=True)
                st.markdown("" + ''.join([f"<span class='badge'>#{t}</span>" for t in tags]), unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            idx += 1

    st.divider()
    st.subheader("📈 세부 점수표")
    st.dataframe(result_df, use_container_width=True)

    # Download CSV
    csv = result_df.to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 추천 결과 CSV로 저장", data=csv, file_name="mbti_career_recommendations.csv", mime="text/csv")

with encyclopedia_tab:
    st.subheader("📚 직업 백과 — 한 눈에 보기")
    st.write("각 직업의 핵심 키워드와 어울리는 MBTI 클러스터를 확인하세요 🧭")

    table_rows = []
    for c in careers:
        clusters = ", ".join([f"{k} {v}/10" for k,v in c['fit'].items()])
        table_rows.append({
            "직업": f"{c['emoji']} {c['name']}",
            "태그": ", ".join(c['tags']),
            "클러스터 적합도": clusters
        })
    st.dataframe(pd.DataFrame(table_rows), use_container_width=True)

    st.info("🔔 팁: 점수는 참고용입니다. 실제 선택은 경험, 가치관, 환경을 함께 고려해요!", icon="💡")

with roadmap_tab:
    st.subheader("🗺️ 나만의 성장 로드맵")
    st.write("선택한 TOP 직업 중 하나를 골라 6단계 로드맵으로 계획해봐요 ✍️")

    choice = st.selectbox("🚀 어떤 직업부터 도전할까요?", options=result_df.head(6)['직업'])
    st.markdown(
        f"""
        <div class='card'>
        <ol>
          <li>🔎 탐색: 관련 유튜브/블로그/강연 3개 시청 & 노트 정리</li>
          <li>📚 기초 학습: 무료 강의/입문서 1권 완독</li>
          <li>🧪 미니 프로젝트: 2주짜리 실습 프로젝트 진행</li>
          <li>🤝 네트워킹: 현업 2명 정보 인터뷰(링크드인/학교 커뮤니티)</li>
          <li>🧰 포트폴리오: 결과 3개 정리해 웹/노션 업로드</li>
          <li>🎯 도전: 인턴/동아리/공모전 1건 지원</li>
        </ol>
        </div>
        """, unsafe_allow_html=True)

    st.success("🌈 한 걸음씩—반짝이는 성장 곡선을 그려봐요!", icon="🌈")

# -------------------- FOOTER --------------------
st.caption("Made with Streamlit 💖 | 이모지 폭탄 🎉 | 교육용 참고 서비스")

