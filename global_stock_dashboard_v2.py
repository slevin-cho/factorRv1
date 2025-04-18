
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go

# 페이지 설정
st.set_page_config(page_title="Global Stock Dashboard", layout="wide")

# 언어 설정
LANGUAGES = {"한국어": "KR", "English": "EN", "日本語": "JP"}
LABELS = {
    "발행주식수": {"KR": "발행주식 수", "EN": "Shares Outstanding", "JP": "発行株式数"},
    "시가총액": {"KR": "시가총액", "EN": "Market Cap", "JP": "時価総額"},
    "최근종가": {"KR": "최근 종가", "EN": "Last Price", "JP": "直近終値"},
    "주식코드입력": {
        "KR": "종목 코드 입력 (예: 삼성전자 → 005930.KS, 다이와증권 → 8601.T, 메드트로닉 → MDT)",
        "EN": "Enter stock code (e.g., 005930.KS, 8601.T, MDT)",
        "JP": "銘柄コードを入力（例：005930.KS、8601.T、MDT）"
    },
    "밸류에이션": {"KR": "밸류에이션 차트", "EN": "Valuation Chart", "JP": "バリュエーションチャート"},
    "PER": {"KR": "PER", "EN": "PER", "JP": "PER"},
    "PBR": {"KR": "PBR", "EN": "PBR", "JP": "PBR"},
    "PSR": {"KR": "PSR", "EN": "PSR", "JP": "PSR"},
    "배당수익률": {"KR": "배당수익률", "EN": "Dividend Yield", "JP": "配当利回り"},
    "단위": {"KR": "단위", "EN": "Unit", "JP": "単位"},
}

lang_select = st.sidebar.selectbox("🌐 Language", list(LANGUAGES.keys()))
LANG = LANGUAGES[lang_select]

st.title("📊 Global Stock Dashboard")

ticker_input = st.text_input(LABELS["주식코드입력"][LANG], value="005930.KS")
if not ticker_input:
    st.stop()

ticker = yf.Ticker(ticker_input)

# 안전하게 info 로딩
try:
    info = ticker.info
except Exception as e:
    st.error("종목 정보를 불러오는 데 실패했습니다.")
    st.stop()

# 기본 정보 메트릭
st.subheader("🔢 " + "기본 정보")
col1, col2, col3 = st.columns(3)

def safe_format(value):
    return f"{value:,.0f}" if isinstance(value, (int, float)) else "N/A"

shares_outstanding = info.get("sharesOutstanding")
market_cap = info.get("marketCap")
current_price = info.get("currentPrice")

col1.metric(LABELS["발행주식수"][LANG], safe_format(shares_outstanding))
col2.metric(LABELS["시가총액"][LANG], safe_format(market_cap))
col3.metric(LABELS["최근종가"][LANG], safe_format(current_price))

# 단위 설정
if ticker_input.endswith(".KS") or ticker_input.endswith(".KQ"):
    unit_label = "억 원 (KRW)"
    unit_div = 1e8
elif ticker_input.endswith(".T"):
    unit_label = "mil. yen (JPY)"
    unit_div = 1e6
else:
    unit_label = "mil. USD"
    unit_div = 1e6

st.markdown(f"📌 **{LABELS['단위'][LANG]}: {unit_label}**")

# 재무제표 표시 함수
def render_financials(title, df):
    if df.empty:
        st.write(f"{title}: N/A")
        return
    df_display = df.div(unit_div).fillna(0).astype(float).applymap(lambda x: f"{x:,.0f}")
    st.write(f"**{title}**")
    st.dataframe(df_display)

# 재무제표 출력
try:
    st.subheader("📑 재무제표")
    render_financials("💰 Balance Sheet", ticker.balance_sheet)
    render_financials("📈 Income Statement", ticker.financials)
    render_financials("💸 Cash Flow", ticker.cashflow)
except Exception as e:
    st.error("재무제표를 불러오지 못했습니다.")

# 밸류에이션 차트
st.sidebar.subheader("📉 " + LABELS["밸류에이션"][LANG])
show_per = st.sidebar.checkbox(LABELS["PER"][LANG], value=True)
show_pbr = st.sidebar.checkbox(LABELS["PBR"][LANG])
show_psr = st.sidebar.checkbox(LABELS["PSR"][LANG])
show_div = st.sidebar.checkbox(LABELS["배당수익률"][LANG])

valuation_data = ticker.history(period="5y", interval="3mo")
valuation_data = valuation_data.dropna()

fig = go.Figure()
if show_per:
    fig.add_trace(go.Scatter(x=valuation_data.index, y=(valuation_data["Close"] / info.get("trailingEps", 1)), mode="lines", name="PER"))
if show_pbr:
    fig.add_trace(go.Scatter(x=valuation_data.index, y=(valuation_data["Close"] / info.get("bookValue", 1)), mode="lines", name="PBR"))
if show_psr:
    fig.add_trace(go.Scatter(x=valuation_data.index, y=(valuation_data["Close"] / info.get("revenuePerShare", 1)), mode="lines", name="PSR"))
if show_div:
    fig.add_trace(go.Scatter(x=valuation_data.index, y=(info.get("dividendYield", 0) * 100), mode="lines", name="배당수익률"))

fig.update_layout(title="Valuation Ratios", height=400, template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)
