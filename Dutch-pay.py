import streamlit as st
import urllib.parse

st.set_page_config(page_title="영근님의 실전 회식 정산기", layout="centered")

# --- 🔗 주소창(URL)에 공유된 정산 결과가 있는지 확인하는 로직 ---
query_params = st.query_params

if "result" in query_params:
    # 📱 단톡방 링크를 타고 들어온 친구들에게 보여주는 전용 화면
    st.title("💰 공유된 정산 리포트")
    encoded_result = query_params["result"]
    # 주소창의 특수문자 깨짐을 원래 글자로 복원(디코딩)
    decoded_result = urllib.parse.unquote(encoded_result)
    
    st.success("단톡방에서 공유된 정산 내역입니다!")
    
    # 전달받은 결과를 줄바꿈 기준으로 예쁘게 출력
    lines = decoded_result.split("\n")
    for line in lines:
        if line.strip():
            st.write(line)
            
    st.divider()
    # 친구들도 자기 폰에서 새로 정산해볼 수 있도록 버튼 제공
    if st.button("🔄 새로 정산하러 가기"):
        st.query_params.clear()
        st.rerun()

else:
    # 🍺 원래 영근님이 사용하시는 정산 입력 화면
    st.title("🍺 Dutch-Pay 계산기")

    # 1. 멤버 설정
    all_members = ["범준", "범수", "승원", "수민", "유현", "가윤"]

    st.info("💡 각 차수별로 참석자와 금액을 입력하면 마지막에 총액을 계산해 드립니다.")

    # 데이터 저장용 변수 (영근님의 5차까지 반영!)
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
    final_report = ""
    
    # 카톡 공유용 텍스트 리포트 만들기
    for name, total in total_summary.items():
        if total > 0:
            final_report += f"👉 **{name}**: {total:,}원\n"
            has_data = True
    
    if has_data:
        grand_total = sum(total_summary.values())
        final_report += f"\n📋 **오늘 총 지출액:** {grand_total:,}원"
        
        st.success("오늘의 정산 리포트입니다!")
        st.markdown(final_report)
        
        # 🚀 [핵심 기능] 주소창에 넣을 공유 링크 생성 로직
        # 마크다운 굵게 표시(**) 태그를 제거하고 주소창용으로 변환(인코딩)
        encoded_report = urllib.parse.quote(final_report.replace("**", "")) 
        
        # 영근님의 실제 앱 주소와 결과를 결합
        share_url = f"https://young-dutch-pay.streamlit.app/?result={encoded_report}"
        
        st.divider()
        st.subheader("🔗 단톡방 공유용 링크")
        # st.code를 쓰면 우측에 '복사 버튼'이 자동으로 생겨서 모바일에서 복사하기 아주 편합니다.
        st.code(share_url, language="text")
        st.info("👆 위 회색 박스 우측의 복사 버튼을 눌러 카톡방에 바로 붙여넣으세요!")
    else:
        st.error("입력된 정산 내역이 없습니다.")
