# 1차 프로토타입용 Streamlit 대시보드 코드
# 주요 종목: 삼성전자, 다이와증권, 메드트로닉

import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# 다국어 지원 세팅
LANG = st.sidebar.selectbox("언어 선택 / Language / 言語", ["한국어", "English", "日本語"])

LABELS = {
    "기업 선택": {"한국어": "기업 선택", "English": "Select Company", "日本語": "企業選択"},
    "발행주식수": {"한국어": "발행주식수", "English": "Shares Outstanding", "日本語": "発行株式数"},
    "시가총액": {"한국어": "시가총액", "English": "Market Cap", "日本語": "時価総額"},
    "최근 종가": {"한국어": "최근 종가", "English": "Latest Price", "日本語": "最新株価"},
    "재무제표": {"한국어": "재무제표", "English": "Financials", "日本語": "財務諸表"},
    "멀티차트": {"한국어": "멀티 밸류에이션 차트", "English": "Valuation Multi Chart", "日本語": "マルチバリュエーションチャート"},
}

# 기본 종목 리스트
companies = {
    "삼성전자 (KR)": "005930.KQ",
    "다이와증권 (JP)": "8601.T",
    "메드트로닉 (US)": "MDT"
}

st.title("📊 글로벌 종목 Fact 리서치 대시보드")

# 기업 선택
selection = st.selectbox(LABELS["기업 선택"][LANG], list(companies.keys()))
ticker = companies[selection]
data = yf.Ticker(ticker)

info = data.info

st.header(selection)
col1, col2, col3 = st.columns(3)
col1.metric(LABELS["발행주식수"][LANG], f"{info.get('sharesOutstanding', 'N/A'):,}")
col2.metric(LABELS["시가총액"][LANG], f"{info.get('marketCap', 'N/A')/1e6:,.0f}M")
col3.metric(LABELS["최근 종가"][LANG], f"{info.get('currentPrice', 'N/A')}")

# 재무제표 출력
st.subheader(LABELS["재무제표"][LANG])
try:
    fin_df = data.financials.T
    st.dataframe(fin_df.style.format("{:,.0f}"))
except:
    st.write("재무제표 데이터를 불러올 수 없습니다.")

# 멀티 밸류에이션 차트
st.subheader(LABELS["멀티차트"][LANG])
chart_options = st.multiselect("차트 항목 선택", ["PER", "PBR", "PSR", "Dividend Yield"], default=["PER", "PBR"])

# 예시용 가짜 데이터
years = [str(y) for y in range(2019, 2024)]
data_map = {
    "PER": [12.1, 15.3, 10.2, 9.8, 13.5],
    "PBR": [1.1, 1.3, 1.0, 1.2, 1.4],
    "PSR": [2.1, 2.4, 2.0, 1.9, 2.3],
    "Dividend Yield": [2.5, 2.4, 2.7, 3.0, 2.8],
}

fig = go.Figure()
for metric in chart_options:
    fig.add_trace(go.Scatter(x=years, y=data_map[metric], mode="lines+markers", name=metric))
fig.update_layout(height=400, template="plotly_dark" if st.get_option("theme.base") == "dark" else "plotly")
st.plotly_chart(fig)

st.markdown("---")
st.caption("프로토타입 버전입니다. 정성 분석 및 추가 항목은 다음 버전에 포함됩니다.")
