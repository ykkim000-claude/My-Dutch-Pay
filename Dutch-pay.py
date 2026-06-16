import streamlit as st
import streamlit.components.v1 as components
import urllib.parse

st.set_page_config(page_title="영근님의 실전 회식 정산기", layout="centered")

# --- 📱 모바일에서 무조건 가로 스크롤을 보장하는 HTML 표 생성 함수 ---
def render_clean_table(round_details_dict, rounds_list):
    table_html = """
    <div style="width: 100%; overflow-x: auto; -webkit-overflow-scrolling: touch; border: 1px solid #e6e9ef; border-radius: 8px; margin: 10px 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
        <table style="width: 100%; min-width: 500px; border-collapse: collapse; table-layout: fixed;">
            <thead>
                <tr style="background-color: #f0f2f6; border-bottom: 2px solid #d1d5db;">
                    <th style="padding: 12px 8px; text-align: left; font-size: 14px; color: #31333f; width: 25%; white-space: nowrap;">차수 [장소]</th>
                    <th style="padding: 12px 8px; text-align: right; font-size: 14px; color: #31333f; width: 20%; white-space: nowrap;">총 금액</th>
                    <th style="padding: 12px 8px; text-align: right; font-size: 14px; color: #31333f; width: 20%; white-space: nowrap;">인당 금액</th>
                    <th style="padding: 12px 12px; text-align: left; font-size: 14px; color: #31333f; width: 35%; white-space: nowrap; padding-left: 20px;">참석자</th>
                </tr>
            </thead>
            <tbody>
    """
    
    has_data = False
    for rd in rounds_list:
        if rd in round_details_dict:
            info = round_details_dict[rd]
            table_html += f"""
            <tr style="border-bottom: 1px solid #e6e9ef;">
                <td style="padding: 12px 8px; font-weight: bold; font-size: 14px; color: #31333f; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{info['차수']} [{info['장소']}]</td>
                <td style="padding: 12px 8px; text-align: right; font-size: 14px; color: #31333f; white-space: nowrap;">{info['총 금액']}</td>
                <td style="padding: 12px 8px; text-align: right; color: #ff4b4b; font-weight: bold; font-size: 14px; white-space: nowrap;">{info['인당 금액']}</td>
                <td style="padding: 12px 12px; text-align: left; font-size: 13px; color: #555555; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; padding-left: 20px;">{info['참석자']}</td>
            </tr>
            """
            has_data = True
            
    table_html += "</tbody></table></div>"
    return table_html if has_data else ""


# --- 🔗 주소창(URL)에 공유된 정산 결과가 있는지 확인하는 로직 ---
query_params = st.query_params

if "result" in query_params:
    st.title("💰 공유된 상세 정산 리포트")
    encoded_result = query_params["result"]
    decoded_result = urllib.parse.unquote(encoded_result)
    
    st.success("단톡방에서 공유된 상세 정산 내역입니다!")
    
    # [공유화면 복원 로직] 표 데이터와 일반 텍스트 데이터를 분리하여 처리
    if "" in decoded_result:
        parts = decoded_result.split("")
        text_before = parts[0]
        table_and_after = parts[1].split("")
        table_part = table_and_after[0]
        text_after = table_and_after[1] if len(table_and_after) > 1 else ""
        
        if text_before.strip():
            st.markdown(text_before)
            
        # 캔버스를 따로 분리하여 표 렌더링 (가로스크롤 완벽 보장)
        components.html(table_part, height=220, scrolling=False)
        
        if text_after.strip():
            st.markdown(text_after)
    else:
        # 구버전 링크 호환용
        st.markdown(decoded_result, unsafe_allow_html=True)
            
    st.divider()
    if st.button("🔄 새로 정산하러 가기"):
        st.query_params.clear()
        st.rerun()

else:
    # 🍺 원래 영근님이 사용하시는 정산 입력 화면
    st.title("🍺 Dutch-Pay 계산기")

    all_members = ["범준", "범수", "승원", "수민", "유현", "가윤"]
    st.info("💡 각 차수별로 참석자와 금액을 입력하면 마지막에 총액을 계산해 드립니다.")

    rounds = ["1차", "2차", "3차", "4차", "5차"]
    total_summary = {name: 0 for name in all_members}
    round_details = {}

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
                
                place_disp = place_name if place_name else "미정"
                members_disp = ", ".join(selected_members)
                round_details[rd] = {
                    "차수": rd,
                    "장소": place_disp,
                    "총 금액": f"{amount:,}원",
                    "인당 금액": f"{dutch_each:,}원",
                    "참석자": members_disp
                }
                
                for name in selected_members:
                    total_summary[name] += dutch_each
            elif amount > 0:
                st.error("참석자를 선택해야 계산이 됩니다!")

st.divider()

st.header("💰 최종 정산 합계")
if st.button("전체 결과 확인하기"):
    table_code = render_clean_table(round_details, rounds)
    
    if table_code:
        st.success("오늘의 상세 정산 리포트가 완성되었습니다!")
        st.markdown("### 📍 차수별 상세 내역")
        
        # 🚀 핵심: 컴포넌트 격리 기술을 사용하여 독립된 iframe 영역에 표를 안전하게 렌더링
        components.html(table_code, height=220, scrolling=False)
        
        # 개인별 최종 송금액 텍스트 생성
        final_report = "### 💳 개인별 최종 송금액\n"
        for name, total in total_summary.items():
            if total > 0:
                final_report += f"👉 **{name}**: {total:,}원\n"
                
        grand_total = sum(total_summary.values())
        final_report += f"\n📋 **오늘 총 지출액:** {grand_total:,}원"
        st.markdown(final_report)
        
        # 🔗 단톡방 공유 데이터 조립 (표 코드가 깨지지 않게 식별자 태그 부착)
        full_report_text = f"{table_code}\n{final_report}"
        encoded_report = urllib.parse.quote(full_report_text) 
        
        share_url = f"https://young-dutch-pay.streamlit.app/?result={encoded_report}"
        
        st.divider()
        st.subheader("🔗 단톡방 공유용 링크")
        st.code(share_url, language="text")
        st.info("👆 위 회색 박스 우측의 복사 버튼을 눌러 카톡방에 바로 붙여넣으세요!")
    else:
        st.error("입력된 정산 내역이 없습니다.")
