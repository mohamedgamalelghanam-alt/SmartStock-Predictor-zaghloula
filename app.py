import streamlit as st
import pandas as pd

st.title("📦 Smart Inventory System")

uploaded_file = st.file_uploader("Upload your data", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, encoding="cp1256")

    df['الكمية'] = pd.to_numeric(df['الكمية'], errors='coerce')
    df['الكمية الحالية'] = pd.to_numeric(df['الكمية الحالية'], errors='coerce')
    df['كمية صغري'] = pd.to_numeric(df['كمية صغري'], errors='coerce')

    stock = df.groupby('الصنف').agg({
        'الكمية الحالية': 'max',
        'كمية صغري': 'max',
        'الكمية': 'mean'
    }).reset_index()

    stock.columns = ['product', 'current_stock', 'min_stock', 'daily_usage']

    stock['days_to_stockout'] = stock['current_stock'] / stock['daily_usage']

    def status(row):
        if row['current_stock'] <= row['min_stock']:
            return "🔴 اطلب فورًا"
        elif row['current_stock'] <= row['min_stock'] * 1.5:
            return "🟡 قريب يخلص"
        else:
            return "🟢 آمن"

    stock['status'] = stock.apply(status, axis=1)

    st.subheader("📊 Stock Analysis")
    st.dataframe(stock.sort_values(by='days_to_stockout'))

    st.subheader("⚠️ المنتجات اللي هتخلص")
    st.dataframe(stock[stock['status'] != "🟢 آمن"])import streamlit as st
import pandas as pd

st.title("📦 Smart Inventory System")

uploaded_file = st.file_uploader("Upload your data", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, encoding="cp1256")

    df['الكمية'] = pd.to_numeric(df['الكمية'], errors='coerce')
    df['الكمية الحالية'] = pd.to_numeric(df['الكمية الحالية'], errors='coerce')
    df['كمية صغري'] = pd.to_numeric(df['كمية صغري'], errors='coerce')

    stock = df.groupby('الصنف').agg({
        'الكمية الحالية': 'max',
        'كمية صغري': 'max',
        'الكمية': 'mean'
    }).reset_index()

    stock.columns = ['product', 'current_stock', 'min_stock', 'daily_usage']

    stock['days_to_stockout'] = stock['current_stock'] / stock['daily_usage']

    def status(row):
        if row['current_stock'] <= row['min_stock']:
            return "🔴 اطلب فورًا"
        elif row['current_stock'] <= row['min_stock'] * 1.5:
            return "🟡 قريب يخلص"
        else:
            return "🟢 آمن"

    stock['status'] = stock.apply(status, axis=1)

    st.subheader("📊 Stock Analysis")
    st.dataframe(stock.sort_values(by='days_to_stockout'))

    st.subheader("⚠️ المنتجات اللي هتخلص")
    st.dataframe(stock[stock['status'] != "🟢 آمن"])