import streamlit as st
import time
from io import StringIO

# ───────────────────── 기본 설정 ─────────────────────
st.set_page_config(page_title="💊 증상별 약 추천 · 단일 선택", page_icon="💊", layout="wide")
st.markdown("""
<style>
:root { --pri:#5b5ce2; --ink:#1f2330; --muted:#6b7280; }
.stApp { background: linear-gradient(180deg, #f5f7ff 0%, #eef4ff 100%); }
.container { max-width: 980px; margin: auto; }
.title { text-align:center; margin: 6px 0 18px; }
.badge { display:inline-block; padding:6px 10px; border-radius:20px; background:#eef1ff; color:#4347c7; font-weight:600; margin-right:8px; }
.step { background:#ffffff; border-radius:16px; padding:18px 20px; box-shadow:0 6px 24px rgba(16,24,40,.06); margin-bottom:16px; }
.card { background:#ffffff; border-radius:16px; padding:18px 20px; box-shadow:0 8px 28px rgba(16,24,40,.08); margin-bottom:14px; }
.hdr { color:var(--ink); margin:0 0 8px; }
.key { color:#111827; font-weight:700; }
.val { color:#374151; }
.hr { height:1px; border:0; background:linear-gradient(90deg, rgba(91,92,226,0) 0%, rgba(91,92,226,.35) 50%, rgba(91,92,226,0) 100%); margin:10px 0 16px; }
.emoji { font-size:46px; text-align:center; animation: pop .55s ease-in-out; }
@keyframes pop { 0%{transform:scale(0)} 55%{transform:scale(1.45)} 100%{transform:scale(1)} }
.redflag { background:#fff1f2; border:1px solid #fecdd3; color:#be123c; padding:10px 12px; border-radius:12px; }
.chips { display:flex; flex-wrap:wrap; gap:8px; }
.chip { background:#eef1ff; color:#3730a3; padding:6px 10px; border-radius:999px; font-size:.92rem; }
.small { color:var(--muted); font-size:.92rem; }
.download { text-align:right; }
</style>
<div class="container">
  <h1 class="title">💊 증상별 약 추천 · 단일 선택</h1>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='container'>", unsafe_allow_html=True)
st.write("⚠️ 이 앱은 **의료 참고용**입니다. 증상이 심하거나 지속되면 반드시 **의료진 상담**을 받으세요.")

# ───────────────────── 데이터 ─────────────────────
DB = {
    "두통": {
        "약": "진통제 (예: 타이레놀, 이부프로펜)",
        "부작용": "속쓰림, 위장 장애, 드물게 간 기능 문제(과량 시)",
        "관리법": "수분 섭취, 화면/눈 휴식, 규칙 수면, 스트레스 관리",
        "복용시간": "증상 시 필요 복용(라벨 지시/최대 용량 준수)",
        "주의사항": "간 질환, 위장 질환자는 복용 전 상담",
        "복용팁": "가능하면 식후 복용해 위장 부담 줄이기",
        "경고": "갑작스런 가장 심한 두통, 신경학적 증상 동반, 72시간 이상 지속 시 진료"
    },
    "편두통": {
        "약": "트립탄 계열(필요 시) + 일반 진통제",
        "부작용": "어지럼, 피로, 드물게 흉부 답답함",
        "관리법": "어두운 환경 휴식, 규칙 수면, 카페인 과다 회피",
        "복용시간": "전구증상/초기에 복용 효과적",
        "주의사항": "심혈관 질환 병력 시 트립탄 사용 전 상담",
        "복용팁": "유발 요인(수면 부족/특정 음식) 기록",
        "경고": "시야장애 지속, 혼동/마비 동반 시 즉시 진료"
    },
    "발열": {
        "약": "해열제 (아세트아미노펜, 이부프로펜)",
        "부작용": "간/위장 부담, 드물게 알레르기",
        "관리법": "수분 보충, 가벼운 복장, 휴식",
        "복용시간": "6–8시간 간격 필요 시(최대 용량 준수)",
        "주의사항": "소아/고령, 간질환자는 용량 주의",
        "복용팁": "체온 38℃ 이상이며 불편할 때 사용",
        "경고": "39.5℃ 이상 고열 지속, 탈수/의식 저하 시 진료"
    },
    "몸살": {
        "약": "해열진통제 + 휴식",
        "부작용": "위장 장애",
        "관리법": "수면/수분, 무리한 운동 지양",
        "복용시간": "증상 시 필요 복용",
        "주의사항": "감염 의심 시 마스크·격리 고려",
        "복용팁": "미온수 샤워로 근육 이완",
        "경고": "호흡곤란, 흉통, 3일↑ 고열 시 진료"
    },
    "기침": {
        "약": "진해제, 거담제 (덱스트로메토르판, 암브록솔)",
        "부작용": "졸림, 어지럼",
        "관리법": "따뜻한 음료, 가습, 휴식",
        "복용시간": "하루 2–3회 필요 시",
        "주의사항": "만 2세 이하 사용 제한 약물 존재",
        "복용팁": "야간 심할 때 취침 전 진해제 활용",
        "경고": "피 섞인 가래, 3주↑ 지속, 호흡곤란 시 진료"
    },
    "가래": {
        "약": "거담제 (암브록솔, 브롬헥신)",
        "부작용": "소화불량, 구역",
        "관리법": "수분 섭취, 가습",
        "복용시간": "라벨 지시",
        "주의사항": "천식/만성폐질환자 복용 전 상담",
        "복용팁": "수분 충분히 함께 섭취",
        "경고": "녹색/악취 가래와 고열 동반 시 진료"
    },
    "목아픔": {
        "약": "진통·소염제, 목 캔디, 가글액",
        "부작용": "위통, 구강 자극",
        "관리법": "따뜻한 물, 휴식, 가습",
        "복용시간": "증상 시",
        "주의사항": "편도 비대/호흡곤란 시 응급",
        "복용팁": "소금물 가글 보조",
        "경고": "고열·침 삼키기 곤란·호흡곤란 시 진료"
    },
    "콧물": {
        "약": "항히스타민제 (로라타딘, 세티리진)",
        "부작용": "졸림, 구강 건조",
        "관리법": "알레르겐 회피, 실내 청결",
        "복용시간": "하루 1회(제제별 상이)",
        "주의사항": "운전·작업 시 주의",
        "복용팁": "취침 전 복용으로 졸림 활용",
        "경고": "안면 통증/고열 동반 시 부비동염 감별"
    },
    "코막힘": {
        "약": "비충혈 완화제, 비강 스프레이",
        "부작용": "불면, 심계항진",
        "관리법": "가습, 생리식염수 세척",
        "복용시간": "단기 사용 권장(국소제는 3일 이내)",
        "주의사항": "고혈압/심질환자 경구제 주의",
        "복용팁": "취침 전엔 국소제 소량",
        "경고": "3일↑ 국소제 사용 시 약물성 비염 위험"
    },
    "알레르기": {
        "약": "항히스타민제 (로라타딘, 펙소페나딘)",
        "부작용": "졸림(1세대), 어지럼",
        "관리법": "원인 회피, 환기",
        "복용시간": "하루 1회(제제별 상이)",
        "주의사항": "임신·수유 중 상담",
        "복용팁": "비수면성(2세대) 우선 고려",
        "경고": "전신 두드러기+호흡곤란=응급"
    },
    "소화불량": {
        "약": "소화제 (베타인, 소화효소제)",
        "부작용": "복통, 설사",
        "관리법": "과식 피하기, 소량씩 자주",
        "복용시간": "식후 또는 증상 시",
        "주의사항": "지속/체중감소 동반 시 검사",
        "복용팁": "자극적 음식·야식 줄이기",
        "경고": "흑색변/혈변, 지속적 구토 시 진료"
    },
    "속쓰림": {
        "약": "제산제, 위산억제제(PPI)",
        "부작용": "설사/변비, 장기 시 흡수 저하",
        "관리법": "식후 바로 눕지 않기, 지방·카페인 줄이기",
        "복용시간": "식전 30분 또는 취침 전",
        "주의사항": "장기 복용 전 상담",
        "복용팁": "증상 심하면 아침/저녁 분복(의사 지시 우선)",
        "경고": "연하곤란·체중감소·흑색변 동반 시 진료"
    },
    "복통": {
        "약": "진경제(부스코판), 위장약, 수분 섭취",
        "부작용": "구갈, 변비",
        "관리법": "자극적 음식 회피, 미온 찜질",
        "복용시간": "증상 시, 라벨 지시",
        "주의사항": "임신·고령, 급성 심한 통증은 평가 필요",
        "복용팁": "가벼운 식사, 수분 유지",
        "경고": "급성 우하복부 통증/발열/구토 지속 시 진료"
    },
    "설사": {
        "약": "지사제(로페라마이드), 경구수분 보충",
        "부작용": "변비, 복부팽만",
        "관리법": "수분·전해질 보충, 자극식 피하기",
        "복용시간": "급성기 단기 사용",
        "주의사항": "혈변·고열 동반 시 지사제 금기",
        "복용팁": "수분 먼저, 지사제는 남용 금지",
        "경고": "탈수(어지럼/소변 감소) 시 진료"
    },
    "변비": {
        "약": "완하제(마그네슘제제 등), 식이섬유",
        "부작용": "복통, 설사, 전해질 불균형(과다 시)",
        "관리법": "수분·섬유질·운동",
        "복용시간": "취침 전 또는 아침(제제별 상이)",
        "주의사항": "장기 남용 금지",
        "복용팁": "규칙적 배변 습관 형성",
        "경고": "혈변·체중감소·철결핍 빈혈 동반 시 진료"
    },
    "피부발진": {
        "약": "항히스타민제, 국소 스테로이드",
        "부작용": "졸림(항히), 피부 얇아짐(장기 스테로이드)",
        "관리법": "원인 회피, 보습",
        "복용시간": "증상 시/단기",
        "주의사항": "광범위·감염 의심 시 진료",
        "복용팁": "연고는 얇게, 필요한 부위만",
        "경고": "입술/혀 붓기·호흡곤란=응급"
    },
    "벌레물림": {
        "약": "항히스타민 연고, 가려움 완화제",
        "부작용": "피부 자극",
        "관리법": "차가운 찜질, 긁지 않기",
        "복용시간": "증상 시",
        "주의사항": "감염·수포 확대 시 진료",
        "복용팁": "외출 후 샤워·의복 털기",
        "경고": "전신 발진/호흡곤란=응급"
    },
    "상처": {
        "약": "소독약(포비돈 요오드), 항생제 연고, 밴드",
        "부작용": "국소 자극, 알레르기",
        "관리법": "깨끗한 물 세척 후 건조, 드레싱 교체",
        "복용시간": "세척→연고→드레싱 순서",
        "주의사항": "깊은 절상/동물 교상은 응급 평가",
        "복용팁": "24–48시간 내 감염징후 확인",
        "경고": "고열·심한 통증·농 배출 시 진료"
    },
    "근육통": {
        "약": "진통·소염제(이부프로펜, 나프록센), 파스",
        "부작용": "위장 장애, 피부 자극, 드물게 신장 영향",
        "관리법": "스트레칭·온찜질·휴식",
        "복용시간": "증상 시(최대 빈도 준수)",
        "주의사항": "신장/위장 질환자는 주의",
        "복용팁": "단기 집중 사용, 장기 연속 피하기",
        "경고": "외상 후 변형/부종·열감 심하면 진료"
    }
}

# ───────────────────── 상태 ─────────────────────
if "history" not in st.session_state:
    st.session_state.history = []

# ───────────────────── 스텝 1: 검색 + 단일 선택 ─────────────────────
st.markdown("<div class='step'>", unsafe_allow_html=True)
st.markdown("<span class='badge'>STEP 1</span> <b>증상 선택</b>", unsafe_allow_html=True)
q = st.text_input("증상 검색(예: 복통, 두통)", "")
options = [k for k in DB.keys() if q.strip() in k] if q else list(DB.keys())
symptom = st.selectbox("한 번에 하나만 선택하세요", [""] + options, index=0)
st.markdown("</div>", unsafe_allow_html=True)

# ───────────────────── 스텝 2: 표시 모드 ─────────────────────
st.markdown("<div class='step'>", unsafe_allow_html=True)
st.markdown("<span class='badge'>STEP 2</span> <b>표시 모드</b>", unsafe_allow_html=True)
mode = st.radio("내용 상세 정도", ["간단 보기", "자세히 보기"], horizontal=True, index=1)
st.markdown("</div>", unsafe_allow_html=True)

# ───────────────────── 스텝 3: 추가하기 ─────────────────────
st.markdown("<div class='step'>", unsafe_allow_html=True)
st.markdown("<span class='badge'>STEP 3</span> <b>결과 추가</b>", unsafe_allow_html=True)
emoji_slot = st.empty()
cols = st.columns([1,1,2])
with cols[0]:
    add = st.button("➕ 카드 추가하기", use_container_width=True)
with cols[1]:
    clear = st.button("🗑️ 전체 삭제", use_container_width=True)
with cols[2]:
    st.markdown("<p class='small'>‘카드 추가하기’를 누르면 아래에 쌓입니다. 각 카드는 개별 삭제 가능.</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

if clear:
    st.session_state.history.clear()
    st.info("모든 카드가 삭제되었습니다.")

if add:
    if not symptom:
        st.warning("증상을 먼저 선택하세요.")
    else:
        emoji_slot.markdown("<div class='emoji'>💊</div>", unsafe_allow_html=True)
        time.sleep(0.5)
        emoji_slot.empty()
        st.session_state.history.append({"증상": symptom, "모드": mode})

# ───────────────────── 결과 영역 ─────────────────────
st.markdown("### 📋 선택된 카드")
if not st.session_state.history:
    st.write("아직 카드가 없습니다. 증상을 선택하고 **카드 추가하기**를 눌러보세요.")
else:
    for i, item in enumerate(st.session_state.history):
        data = DB[item["증상"]]
        simple = (item["모드"] == "간단 보기")

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        top = st.columns([6,1,1])
        with top[0]:
            st.markdown(f"<h3 class='hdr'>🩺 {item['증상']}</h3>", unsafe_allow_html=True)
        with top[1]:
            if st.button("삭제", key=f"del_{i}"):
                del st.session_state.history[i]
                st.experimental_rerun()
        with top[2]:
            # 다운로드 텍스트 만들기
            buf = StringIO()
            buf.write(f"[{item['증상']}]\n")
            buf.write(f"- 약: {data['약']}\n")
            buf.write(f"- 부작용: {data['부작용']}\n")
            if not simple:
                buf.write(f"- 관리법: {data['관리법']}\n")
                buf.write(f"- 복용시간: {data['복용시간']}\n")
                buf.write(f"- 주의사항: {data['주의사항']}\n")
                buf.write(f"- 복용팁: {data['복용팁']}\n")
                buf.write(f"- 경고: {data['경고']}\n")
            st.download_button("⬇️ 메모 저장", data=buf.getvalue(), file_name=f"{item['증상']}_안내.txt", mime="text/plain")

        st.markdown("<hr class='hr'/>", unsafe_allow_html=True)
        st.markdown(f"<span class='key'>💊 약</span> : <span class='val'>{data['약']}</span>", unsafe_allow_html=True)
        st.markdown(f"<span class='key'>⚠️ 부작용</span> : <span class='val'>{data['부작용']}</span>", unsafe_allow_html=True)

        if not simple:
            st.markdown(f"<span class='key'>📝 관리법</span> : <span class='val'>{data['관리법']}</span>", unsafe_allow_html=True)
            st.markdown(f"<span class='key'>🕒 복용 시간</span> : <span class='val'>{data['복용시간']}</span>", unsafe_allow_html=True)
            st.markdown(f"<span class='key'>❗ 주의사항</span> : <span class='val'>{data['주의사항']}</span>", unsafe_allow_html=True)
            st.markdown(f"<span class='key'>💡 복용 팁</span> : <span class='val'>{data['복용팁']}</span>", unsafe_allow_html=True)
            st.markdown(f"<div class='redflag'><b>🚩 이런 경우 즉시 진료:</b> {data['경고']}</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

# 선택된 증상 칩 표시
if st.session_state.history:
    st.markdown("#### 🔖 선택 기록")
    st.markdown("<div class='chips'>" + "".join([f"<span class='chip'>{h['증상']}</span>" for h in st.session_state.history]) + "</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)  # /container
