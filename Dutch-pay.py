import streamlit as st

st.set_page_config(page_title="영근님의 실전 회식 정산기", layout="centered")

st.title("🍺 Dutch-Pay 계산기")

# 1. 멤버 설정 (수정된 명단입니다!)
all_members = ["범준", "범수", "승원", "수민", "유현", "가윤"]

st.info("💡 각 차수별로 참석자와 금액을 입력하면 마지막에 총액을 계산해 드립니다.")

# 데이터 저장용 변수
rounds = ["1차", "2차", "3차", "4차", "5차"]
total_summary = {name: 0 for name in all_members}

for rd in rounds:
    with st.expander(f"📍 {rd} 정산하기", expanded=True):
        place_name = st.text_input(f"{rd} 장소 이름", placeholder="예: 삼겹살집, 치킨집", key=f"place_{rd}")
        
        st.write(f"👉 {rd} 참석자 선택:")
        selected_members = []
        cols = st.columns(len(all_members))
        for i, name in enumerate(all_members):
            with cols[i]:
                if st.checkbox(name, key=f"check_{rd}_{name}"):
                    selected_members.append(name)
        
        amount = st.number_input(f"{rd} 결제 금액 (원)", min_value=0, step=1000, key=f"amount_{rd}")
        
        if len(selected_members) > 0 and amount > 0:
            dutch_each = amount // len(selected_members)
            st.warning(f"✅ {rd} 결과: 인당 {dutch_each:,}원 ({len(selected_members)}명)")
            for name in selected_members:
                total_summary[name] += dutch_each
        elif amount > 0:
            st.error("참석자를 선택해야 계산이 됩니다!")

st.divider()

st.header("💰 최종 정산 합계")
if st.button("전체 결과 확인하기"):
    has_data = False
    final_list = []
    for name, total in total_summary.items():
        if total > 0:
            final_list.append(f"**{name}**: {total:,}원")
            has_data = True
    
    if has_data:
        st.success("오늘의 정산 리포트입니다!")
        for line in final_list:
            st.write(line)
        grand_total = sum(total_summary.values())
        st.info(f"📋 **오늘 총 지출액:** {grand_total:,}원")
    else:
        st.error("입력된 정산 내역이 없습니다.")
