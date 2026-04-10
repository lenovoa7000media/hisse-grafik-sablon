import streamlit as st
import yfinance as yf
import pandas as pd
import mplfinance as mpf

st.set_page_config(page_title="Hisse Grafiği Şablonu", layout="wide")
st.title("📈 Hisse Grafiği Şablonu")

# Hisse sembolü girişi
hisse = st.text_input("Hisse sembolü girin", "AAPL").upper()

# İndikatörleri sabit tut
if hisse:
    st.write(f"Veriler yükleniyor: {hisse}")
    try:
        # Son 6 ay günlük veri
        df = yf.download(hisse, period="6mo", interval="1d")
        if df.empty:
            st.warning("Hisse bulunamadı veya veri yok.")
        else:
            # EMA50 ve EMA200
            df['EMA50'] = df['Close'].ewm(span=50, adjust=False).mean()
            df['EMA200'] = df['Close'].ewm(span=200, adjust=False).mean()
            
            # Basit RSI
            delta = df['Close'].diff()
            gain = delta.clip(lower=0)
            loss = -delta.clip(upper=0)
            avg_gain = gain.rolling(14).mean()
            avg_loss = loss.rolling(14).mean()
            rs = avg_gain / avg_loss
            df['RSI'] = 100 - (100 / (1 + rs))
            
            st.write("📊 Grafik")
            mpf.plot(df, type='candle', style='yahoo',
                     mav=(50, 200), volume=True, show_nontrading=True)
            
            st.write("✅ EMA50, EMA200 ve RSI hesaplandı.")
    except Exception as e:
        st.error(f"Hata oluştu: {e}")
