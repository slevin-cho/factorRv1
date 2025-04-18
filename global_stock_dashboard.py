
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# 기본 설정
st.set_page_config(layout="wide", page_title="Global Stock Dashboard", page_icon=":bar_chart:")

# 다국어 지원
LANGUAGES = {"한국어": "KR", "English": "EN", "日本語": "JP"}
LABELS = {
    "발행주식수": {"KR": "발행주식 수", "EN": "Shares Outstanding", "JP": "発行株式数"},
    "시가총액": {"KR": "시가총액", "EN": "Market Cap", "JP": "時価総額"},
    "최근종가": {"KR": "최근 종가", "EN": "Last Price", "JP": "直近終値"},
    "선택": {"KR": "선택", "EN": "Select", "JP": "選択"},
    "주식코드입력": {"KR": "종목 코드 입력 (예: 삼성전자 → 005930.KS, Medtronic → MDT)", 
                    "EN": "Enter stock code (e.g., 005930.KS for Samsung, MDT for Medtronic)", 
                    "JP": "銘柄コードを入力（例：サムスン → 005930.KS、メドトロニック → MDT）"},
}

# 언어 선택
lang_select = st.sidebar.selectbox("🌐 Language", list(LANGUAGES.keys()))
LANG = LANGUAGES[lang_select]

st.title("📊 Global Stock Dashboard")
ticker_input = st.text_input(LABELS["주식코드입력"][LANG], value="005930.KS")

if ticker_input:
    ticker = yf.Ticker(ticker_input)
    info = ticker.info

    # 메트릭 표시
    st.subheader("🔢 기본 정보")
    col1, col2, col3 = st.columns(3)

    # 안전한 숫자 포맷팅
    shares_outstanding = info.get("sharesOutstanding")
    market_cap = info.get("marketCap")
    current_price = info.get("currentPrice")

    col1.metric(
        LABELS["발행주식수"][LANG],
        f"{shares_outstanding:,}" if shares_outstanding else "N/A"
    )
    col2.metric(
        LABELS["시가총액"][LANG],
        f"{market_cap:,}" if market_cap else "N/A"
    )
    col3.metric(
        LABELS["최근종가"][LANG],
        f"{current_price:,}" if current_price else "N/A"
    )

    # 재무제표
    st.subheader("📈 재무제표")
    try:
        annual_bs = ticker.balance_sheet
        annual_is = ticker.financials
        annual_cf = ticker.cashflow

        st.write("**[연결 기준 Balance Sheet]**")
        st.dataframe(annual_bs)

        st.write("**[연결 기준 Income Statement]**")
        st.dataframe(annual_is)

        st.write("**[연결 기준 Cashflow Statement]**")
        st.dataframe(annual_cf)
    except Exception as e:
        st.error(f"재무 데이터를 불러오는 데 실패했습니다: {e}")
