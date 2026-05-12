import streamlit as st

st.title("🍺 영근님의 간편 정산기")

all_members = ["영근", "멤버1", "멤버2", "멤버3", "멤버4", "멤버5"]

st.subheader("1. 참석자를 선택하세요")
selected_members = []
cols = st.columns(3)

for i, name in enumerate(all_members):
    with cols[i % 3]:
        if st.checkbox(name, key=name):
            selected_members.append(name)

st.subheader("2. 결제 금액을 입력하세요")
total_amount = st.number_input("총 금액 (원)", min_value=0, step=1000)

if st.button("N분의 1 계산하기"):
    member_count = len(selected_members)
    if member_count > 0:
        dutch_pay = total_amount // member_count
        st.success(f"총 {member_count}명이 참석하셨네요!")
        st.info(f"인당 지불할 금액은 **{dutch_pay:,}원** 입니다.")
        st.write("👉 입금 대상자:", ", ".join(selected_members))
    else:
        st.error("참석자를 최소 1명 이상 선택해 주세요!")
