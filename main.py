import streamlit as st
import pandas as pd
import random, time
from datetime import datetime

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="뭐 먹을까? 🍽️ 룰렛", 
    page_icon="🎡",
    layout="wide", 
    initial_sidebar_state="expanded"
)

# -------------------- CUSTOM STYLES --------------------
st.markdown(
    r"""
    <style>
    .stApp { 
        background: radial-gradient(1200px 600px at 20% 10%, rgba(255,255,255,0.08), transparent),
                    linear-gradient(120deg, #120c56 0%, #5b2a86 35%, #a4508b 70%, #0b132b 100%);
        color: #f8f9ff;
    }
    .title { font-weight: 900; font-size: 2.2rem; letter-spacing: 0.6px; }
    .gradient-text {
        background: linear-gradient(90deg, #ffd166, #ff6b6b, #845ec2, #00c9a7);
        -webkit-background-clip: text; background-clip: text; color: transparent;
        text-shadow: 0 0 18px rgba(255,255,255,0.15);
    }
    .card { background: rgba(255,255,255,0.07); border: 1px solid rgba(255,255,255,0.22); border-radius: 18px; padding: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.35); }
    .badge { display: inline-block; padding: 4px 10px; border-radius: 999px; margin: 4px 6px 0 0; background: linear-gradient(135deg, rgba(255,255,255,0.18), rgba(255,255,255,0.08)); border: 1px solid rgba(255,255,255,0.25); font-size: 0.78rem; }
    .tiny { font-size: 0.82rem; opacity: 0.92; }
    .wheel { font-size: 2.6rem; height: 3.2rem; display:flex; align-items:center; justify-content:center; }

    /* Confetti emoji */
    .emoji-sky { position: fixed; left:0; top:0; pointer-events:none; width:100%; height:0; z-index:9999; }
    .fall { position:absolute; top:-2rem; font-size:1.6rem; animation: fall 7s linear forwards; filter: drop-shadow(0 6px 8px rgba(0,0,0,0.4)); }
    @keyframes fall { to { transform: translateY(160vh) rotate(360deg);} }

    section[data-testid="stSidebar"] > div { background: rgba(0,0,0,0.35); }
    .stDataFrame { border-radius: 16px; overflow: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------- FUN: EMOJI SKY (first load) ---------------
emo = list("🍣🍜🍕🍔🌮🥗🍗🍛🍙🍤🥟🍞🍝🍰🍩🍟🌯🧋☕🍊🍓🍫🧇🥪🍱🥞🧀🥨🥡🥘🥠🧁")
if 'rained' not in st.session_state:
    st.session_state['rained'] = True
    drops = ''.join([
        f'<span class="fall" style="left:{random.randint(0,100)}%; animation-delay:{random.random()*2:.2f}s">{random.choice(emo)}</span>'
        for _ in range(70)
    ])
    st.markdown(f'<div class="emoji-sky">{drops}</div>', unsafe_allow_html=True)

# -------------------- HEADER --------------------
col1, col2 = st.columns([0.82, 0.18])
with col1:
    st.markdown("""
    <div class='title gradient-text'>🎡 What Should I Eat? — 초초 화려한 음식 추천기 🍽️✨</div>
    <div class='tiny'>기분 · 예산 · 매움 · 식단 취향으로 찰떡 메뉴를 골라드려요! 오늘은 <b>맛있는 선택</b>만 하자 🍀</div>
    """, unsafe_allow_html=True)
with col2:
    st.metric("오늘", datetime.now().strftime("%Y-%m-%d"), delta="배고픔 +100 🍚")

st.divider()

# -------------------- DATA --------------------
foods = [
    {"name":"낙곱새","emoji":"🥘","cuisine":"Korean","diet":"normal","spice":4,"price":"₩","kcal":480,"tags":["soup","rice","spicy"]},
    {"name":"비빔밥","emoji":"🥗","cuisine":"Korean","diet":"vegetarian","spice":2,"price":"₩₩","kcal":550,"tags":["rice","veggie"]},
    {"name":"불고기","emoji":"🍖","cuisine":"Korean","diet":"normal","spice":1,"price":"₩₩₩","kcal":650,"tags":["meat","rice"]},
    {"name":"된장찌개","emoji":"🍲","cuisine":"Korean","diet":"normal","spice":1,"price":"₩","kcal":420,"tags":["soup","rice"]},
    {"name":"초밥","emoji":"🍣","cuisine":"Japanese","diet":"pescatarian","spice":0,"price":"₩₩₩","kcal":520,"tags":["seafood","rice","cold"]},
    {"name":"라멘","emoji":"🍜","cuisine":"Japanese","diet":"normal","spice":2,"price":"₩₩","kcal":700,"tags":["noodle","soup"]},
    {"name":"우동","emoji":"🥢","cuisine":"Japanese","diet":"normal","spice":0,"price":"₩₩","kcal":620,"tags":["noodle","soup"]},
    {"name":"짜장면","emoji":"🍜","cuisine":"Chinese","diet":"normal","spice":0,"price":"₩","kcal":720,"tags":["noodle"]},
    {"name":"짬뽕","emoji":"🔥","cuisine":"Chinese","diet":"normal","spice":4,"price":"₩₩","kcal":680,"tags":["noodle","spicy","soup"]},
    {"name":"마파두부","emoji":"🥡","cuisine":"Chinese","diet":"vegetarian","spice":3,"price":"₩₩","kcal":520,"tags":["tofu","spicy","rice"]},
    {"name":"피자","emoji":"🍕","cuisine":"Italian","diet":"normal","spice":0,"price":"₩₩₩","kcal":800,"tags":["share","cheese"]},
    {"name":"파스타","emoji":"🍝","cuisine":"Italian","diet":"normal","spice":1,"price":"₩₩₩","kcal":730,"tags":["noodle","cheese"]},
    {"name":"타코","emoji":"🌮","cuisine":"Mexican","diet":"normal","spice":3,"price":"₩₩","kcal":600,"tags":["handhold","spicy"]},
    {"name":"부리또","emoji":"🌯","cuisine":"Mexican","diet":"normal","spice":2,"price":"₩₩","kcal":780,"tags":["rice","handhold"]},
    {"name":"버거","emoji":"🍔","cuisine":"Western","diet":"normal","spice":1,"price":"₩₩","kcal":750,"tags":["handhold","share"]},
    {"name":"스테이크","emoji":"🥩","cuisine":"Western","diet":"normal","spice":0,"price":"₩₩₩","kcal":680,"tags":["meat"]},
    {"name":"팟타이","emoji":"🍝","cuisine":"Thai","diet":"normal","spice":2,"price":"₩₩","kcal":690,"tags":["noodle","sweet"]},
    {"name":"쌀국수","emoji":"🍜","cuisine":"Vietnamese","diet":"normal","spice":1,"price":"₩₩","kcal":520,"tags":["noodle","soup"]},
    {"name":"반미","emoji":"🥖","cuisine":"Vietnamese","diet":"normal","spice":1,"price":"₩","kcal":560,"tags":["bread","handhold"]},
    {"name":"카레","emoji":"🍛","cuisine":"Indian","diet":"vegetarian","spice":3,"price":"₩₩","kcal":700,"tags":["rice","spicy"]},
    {"name":"팔라펠 랩","emoji":"🧆","cuisine":"MiddleEastern","diet":"vegan","spice":2,"price":"₩₩","kcal":610,"tags":["veggie","handhold"]},
    {"name":"샐러드","emoji":"🥗","cuisine":"Global","diet":"vegan","spice":0,"price":"₩₩","kcal":380,"tags":["veggie","light"]},
    {"name":"치킨","emoji":"🍗","cuisine":"Korean","diet":"normal","spice":2,"price":"₩₩","kcal":900,"tags":["share","fried"]},
    {"name":"만두","emoji":"🥟","cuisine":"Korean","diet":"normal","spice":0,"price":"₩","kcal":520,"tags":["steam","snack"]},
    {"name":"크레페","emoji":"🥞","cuisine":"French","diet":"vegetarian","spice":0,"price":"₩₩","kcal":450,"tags":["sweet","dessert"]},
    {"name":"아사이볼","emoji":"🍧","cuisine":"Cafe","diet":"vegan","spice":0,"price":"₩₩","kcal":320,"tags":["sweet","light"]},
    {"name":"티라미수","emoji":"🍰","cuisine":"Italian","diet":"vegetarian","spice":0,"price":"₩₩","kcal":420,"tags":["dessert","sweet"]},
    {"name":"스시동","emoji":"🍱","cuisine":"Japanese","diet":"pescatarian","spice":0,"price":"₩₩₩","kcal":640,"tags":["seafood","rice"]},
    {"name":"콩불","emoji":"🥘","cuisine":"Korean","diet":"normal","spice":4,"price":"₩₩","kcal":780,"tags":["spicy","meat","rice"]},
    {"name":"나시고렝","emoji":"🍚","cuisine":"Indonesian","diet":"normal","spice":2,"price":"₩₩","kcal":720,"tags":["rice","fried"]},
]

df = pd.DataFrame(foods)

# -------------------- SIDEBAR FILTERS --------------------
st.sidebar.title("🎛️ 취향 필터")
select_cuisines = st.sidebar.multiselect("🍱 음식 종류", sorted(df['cuisine'].unique()), default=[])
diet = st.sidebar.multiselect("🥦 식단", ["normal","vegetarian","vegan","pescatarian"], default=[])
max_spice = st.sidebar.slider("🌶️ 매운맛 허용치", 0, 5, 5)
price = st.sidebar.multiselect("💸 예산", ["₩","₩₩","₩₩₩"], default=[])
cal_min, cal_max = st.sidebar.slider("🔥 칼로리 범위", 250, 1200, (300, 900))
keywords = st.sidebar.multiselect("🏷️ 키워드", sorted({t for tags in df['tags'] for t in tags}), default=[])

st.sidebar.caption("필터를 비우면 더 다양하게 추천해요 ✨")

# -------------------- FILTER LOGIC --------------------
filtered = df.copy()
if select_cuisines:
    filtered = filtered[filtered['cuisine'].isin(select_cuisines)]
if diet:
    filtered = filtered[filtered['diet'].isin(diet)]
filtered = filtered[filtered['spice'] <= max_spice]
if price:
    filtered = filtered[filtered['price'].isin(price)]
filtered = filtered[(filtered['kcal'] >= cal_min) & (filtered['kcal'] <= cal_max)]
if keywords:
    filtered = filtered[filtered['tags'].apply(lambda x: any(k in x for k in keywords))]

# -------------------- STATE --------------------
if 'history' not in st.session_state:
    st.session_state['history'] = []
if 'favorites' not in st.session_state:
    st.session_state['favorites'] = []

# -------------------- TABS --------------------
roulette_tab, explore_tab, plan_tab, fav_tab = st.tabs(["🎡 룰렛", "🔎 탐색", "🗓️ 밀플랜", "⭐ 즐겨찾기"])

# -------------------- ROULETTE --------------------
with roulette_tab:
    st.subheader("🎡 오늘의 메뉴 룰렛 — 버튼을 누르면 스핀이 시작! ✨")
    slot = st.empty()

    colA, colB, colC = st.columns([0.4, 0.3, 0.3])
    choice = None
    with colA:
        if st.button("🎰 룰렛 돌리기!", type="primary"):
            pool = filtered if not filtered.empty else df
            # spin visual
            for i in range(22):
                item = pool.sample(1).iloc[0]
                slot.markdown(f"<div class='wheel'>{item['emoji']} <b>{item['name']}</b></div>", unsafe_allow_html=True)
                time.sleep(0.06 + i*0.01)
            choice = item
            st.session_state['history'].insert(0, f"{item['emoji']} {item['name']}")
            if len(st.session_state['history']) > 20:
                st.session_state['history'].pop()
            # confetti
            st.balloons()
            st.toast("맛있는 하루 가즈아!", icon="🍽️")

    with colB:
        if st.button("🔁 아무거나(필터무시)"):
            item = df.sample(1).iloc[0]
            slot.markdown(f"<div class='wheel'>{item['emoji']} <b>{item['name']}</b></div>", unsafe_allow_html=True)
            st.session_state['history'].insert(0, f"{item['emoji']} {item['name']}")
            st.balloons()
    with colC:
        if st.button("🎯 건강하게 추천(≤600kcal)"):
            pool = (filtered if not filtered.empty else df)
            pool = pool[pool['kcal'] <= 600]
            if pool.empty:
                pool = df[df['kcal'] <= 600]
            item = pool.sample(1).iloc[0]
            slot.markdown(f"<div class='wheel'>{item['emoji']} <b>{item['name']}</b></div>", unsafe_allow_html=True)
            st.session_state['history'].insert(0, f"{item['emoji']} {item['name']}")
            st.balloons()

    st.markdown("---")
    st.markdown("**최근 룰렛 결과**")
    if st.session_state['history']:
        cols = st.columns(6)
        for i, h in enumerate(st.session_state['history'][:12]):
            with cols[i%6]:
                st.markdown(f"<div class='card tiny'>{h}</div>", unsafe_allow_html=True)
    else:
        st.caption("아직 결과가 없네요. 룰렛을 돌려보세요! 🎡")

# -------------------- EXPLORE --------------------
with explore_tab:
    st.subheader("🔎 메뉴 탐색 — 카드 클릭으로 ⭐ 즐겨찾기 저장")
    show_df = filtered if not filtered.empty else df

    n = len(show_df)
    cols_per_row = 4
    rows = (n + cols_per_row - 1) // cols_per_row
    idx = 0
    for r in range(rows):
        cols = st.columns(cols_per_row)
        for c in cols:
            if idx >= n: break
            row = show_df.iloc[idx]
            with c:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown(f"<h3 class='gradient-text' style='font-size:1.1rem'>{row['emoji']} {row['name']}</h3>", unsafe_allow_html=True)
                st.markdown(f"<div class='tiny'>🍱 {row['cuisine']} · 🔥 {row['spice']} · 💸 {row['price']} · 🔥kcal {row['kcal']}</div>", unsafe_allow_html=True)
                st.markdown(''.join([f"<span class='badge'>#{t}</span>" for t in row['tags']]), unsafe_allow_html=True)
                if st.button(f"⭐ {row['name']} 저장", key=f"fav_{row['name']}"):
                    val = f"{row['emoji']} {row['name']}"
                    if val not in st.session_state['favorites']:
                        st.session_state['favorites'].insert(0, val)
                        st.toast("즐겨찾기에 담았어요!", icon="⭐")
                st.markdown("</div>", unsafe_allow_html=True)
            idx += 1

    st.markdown("---")
    st.caption("팁: 왼쪽 필터로 취향을 좁힌 뒤 저장하면, 나만의 메뉴 북 완성 ✨")

# -------------------- MEAL PLAN --------------------
with plan_tab:
    st.subheader("🗓️ 7일 밀플랜 — 균형 잡힌 일주일 메뉴 ✨")
    base = filtered if not filtered.empty else df
    if len(base) < 7:
        base = df
    if st.button("🧠 자동 생성"):
        picks = base.sample(7, replace=False) if len(base) >= 7 else base.sample(7, replace=True)
        days = ["월","화","수","목","금","토","일"]
        plan_df = pd.DataFrame({
            "요일": days,
            "메뉴": [f"{r['emoji']} {r['name']}" for _, r in picks.iterrows()],
            "칼로리": [int(r['kcal']) for _, r in picks.iterrows()],
            "매움": [int(r['spice']) for _, r in picks.iterrows()],
        })
        st.dataframe(plan_df, use_container_width=True)
        csv = plan_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 밀플랜 CSV 저장", data=csv, file_name="meal_plan_7days.csv", mime="text/csv")

# -------------------- FAVORITES --------------------
with fav_tab:
    st.subheader("⭐ 나의 즐겨찾기")
    if st.session_state['favorites']:
        cols = st.columns(5)
        for i, f in enumerate(st.session_state['favorites'][:20]):
            with cols[i%5]:
                st.markdown(f"<div class='card tiny'>{f}</div>", unsafe_allow_html=True)
        if st.button("🧹 모두 지우기"):
            st.session_state['favorites'] = []
            st.toast("비웠어요!", icon="🧹")
    else:
        st.caption("아직 즐겨찾기가 없어요. 탐색 탭에서 ⭐ 버튼으로 추가!")

# -------------------- FOOTER --------------------
st.divider()
st.caption("Made with Streamlit 💖 | 이모지 폭발 🍣🎆 | 오늘도 맛있게 ✨")
