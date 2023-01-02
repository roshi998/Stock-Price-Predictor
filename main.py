import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
from urllib.request import Request,urlopen

st.write("""
Stock market web application by **ROSHAN RAJ CHAURASIA**  
**Visually** show data on a stock! Date range from Market

""")
st.sidebar.header('User Input')
start_date = st.sidebar.text_input("Start Date", "2015-01-01")
end_date = st.sidebar.text_input("End Date", "2022-3-9")
stock_symbol = st.sidebar.text_input("Stock Symbol", "ITC")
TICKER=stock_symbol
stock_symbol.upper()
TICKER+=".NS"
TICKER.upper()

#for fundamental data
req=Request(f"https://ticker.finology.in/company/{stock_symbol}")
webpage=urlopen(req)
data=pd.read_html(webpage,header=0)

pf=yf.Ticker(TICKER)
nf=yf.Ticker('^NSEI')
change=((nf.info['regularMarketPrice']-nf.info["regularMarketPreviousClose"])/nf.info["regularMarketPreviousClose"])*100
ch=str(round(change, 2))
ch+="%"
bf=yf.Ticker('^BSESN')

bhange=((bf.info['regularMarketPrice']-bf.info["regularMarketPreviousClose"])/bf.info["regularMarketPreviousClose"])*100
bh=str(round(bhange, 2))
bh+="%"
col1, col2 = st.columns(2)
col1.metric(label="NIFTY 50", value=nf.info["regularMarketPrice"], delta=ch)
col2.metric(label="SENSEX", value=bf.info["regularMarketPrice"], delta=bh)

nsedf = yf.download('^NSEI',start_date,end_date)
bsedf = yf.download('^BSESN',start_date,end_date)
chart_data = pd.DataFrame(
     nsedf['Close'],bsedf['Close'],
     columns=['NIFTY 50', 'SENSEX'])
# st.line_chart(chart_data)
nsedf = yf.download('^NSEI',start_date,end_date)
# st.line_chart(nsedf['Close'],bsedf['Close'])
bsedf = yf.download('^BSESN',start_date,end_date)
st.line_chart(bsedf['Close'])

st.title(pf.info["longName"])
change=((pf.info["currentPrice"]-pf.info["previousClose"])/pf.info["previousClose"])*100
ch=str(round(change, 2))
ch+="%"
st.metric(label="Current Price", value=pf.info["currentPrice"], delta=ch)
st.write("Sector:- ",pf.info["sector"])
st.write("52 Week High-",pf.info["fiftyTwoWeekHigh"],"\t52 Week Low-",pf.info["fiftyTwoWeekLow"])
st.write("Recommendations:",pf.info["recommendationKey"])
st.write("Industry:-",pf.info["industry"])

st.header("Line chart ")
df = yf.download(TICKER,start_date,end_date)
newdf = df.reset_index()
st.line_chart(df['Close'])
st.header("Candlestick Chart")
# moving average
exp12 = newdf['Close'].ewm(span=12, adjust=False).mean()
exp26 = newdf['Close'].ewm(span=26, adjust=False).mean()
macd = exp12 - exp26
signal = macd.ewm(span=9, adjust=False).mean()


# Create subplots and mention plot grid size
# Create subplots and mention plot grid size
fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
               vertical_spacing=0.03, subplot_titles=(f'{TICKER}', 'Volume'),
               row_width=[0.3,0.2, 0.7])

# Plot OHLC on 1st row
fig.add_trace(go.Candlestick(x=newdf["Date"], open=newdf["Open"], high=newdf["High"],
                low=newdf["Low"], close=newdf["Close"], name="OHLC"),
                row=1, col=1
)
# Bar trace for volumes on 2nd row without legend
fig.add_trace(go.Scatter(x=newdf['Date'], y=exp12, name='Moving Avg 12',
                        line=dict(color='royalblue',width=2)))
fig.add_trace(go.Scatter(x=newdf['Date'], y=exp26, name='Moving Avg 26',
                        line=dict(color='firebrick',width=2)))
fig.add_trace(go.Bar(x=newdf['Date'], y=newdf['Volume'], showlegend=False), row=2, col=1)

# Do not show OHLC's rangeslider plot
fig.update(layout_xaxis_rangeslider_visible=False)
fig.update_layout(
    autosize=False,
    width=850,
    height=850,)
st.plotly_chart(fig, use_container_width=False)

st.subheader("About the company")
st.write(pf.info["longBusinessSummary"])

st.header("Financial data")
st.subheader("Quarterly Result (All Figures in Cr.)")
df1 = pd.DataFrame(data[1])
df1=df1.style.hide_index()
st.table(df1)

st.subheader("Profit & Loss (All Figures in Cr. Adjusted EPS in Rs.)")
df2 = pd.DataFrame(data[2])
df2=df2.style.hide_index()
st.table(df2)

st.subheader("Balance Sheet (All Figures are in Crores.)")
df3 = pd.DataFrame(data[3])
df_1 = data[3].iloc[:7,:]
df_2 = data[3].iloc[7:,:]
df_3 = df_1.replace(np.nan, "")
df_4 = df_2.replace(np.nan, "")
# df_3=df_1.style.hide_index()
# df_4=df_2.style.hide_index()
# st.table(df_3)
# st.table(df_4)

st.subheader("Cash Flows (All Figures are in Crores.)")
df4 = pd.DataFrame(data[4])
df4=df4.style.hide_index()
st.table(df4)

# "sector","city","country","phone",
# st.write(pf.recommendations)
st.write(pf.actions)
st.subheader('Shareholding')
st.write(pf.institutional_holders)
sh = pf.major_holders.reset_index()
st.subheader("Sharehoding in percentage")
st.write(sh)
st.subheader("Calendar")
st.write(pf.calendar)
st.subheader("Price Dataset")
st.write(newdf)
# st.write(pf.info)





