import streamlit as st
import pandas as pd

# إعداد الصفحة وتغيير الثيم للـ Dark Mode بشكل برمجي (اختياري)
st.set_page_config(page_title="Smart Inventory System", layout="wide")

st.title("📦 Smart Inventory System")

uploaded_file = st.file_uploader("Upload your data (CSV)", type=["csv"])

if uploaded_file:
    try:
        # محاولة القراءة بترميز cp1256 للعربي، وإذا فشل يستخدم utf-8
        try:
            df = pd.read_csv(uploaded_file, encoding="cp1256")
        except:
            df = pd.read_csv(uploaded_file, encoding="utf-8")

        # تحويل البيانات لأرقام مع معالجة الأخطاء
        df['الكمية'] = pd.to_numeric(df['الكمية'], errors='coerce')
        df['الكمية الحالية'] = pd.to_numeric(df['الكمية الحالية'], errors='coerce')
        df['كمية صغري'] = pd.to_numeric(df['كمية صغري'], errors='coerce')

        # تجميع البيانات حسب الصنف
        stock = df.groupby('الصنف').agg({
            'الكمية الحالية': 'max',
            'كمية صغري': 'max',
            'الكمية': 'mean'
        }).reset_index()

        stock.columns = ['product', 'current_stock', 'min_stock', 'daily_usage']

        # حساب الأيام المتوقعة لنفاذ المخزون
        stock['days_to_stockout'] = stock['current_stock'] / stock['daily_usage']

        def status(row):
            if row['current_stock'] <= row['min_stock']:
                return "🔴 اطلب فورًا"
            elif row['current_stock'] <= row['min_stock'] * 1.5:
                return "🟡 قريب يخلص"
            else:
                return "🟢 آمن"

        stock['status'] = stock.apply(status, axis=1)

        # عرض النتائج
        st.subheader("📊 Stock Analysis")
        st.dataframe(stock.sort_values(by='days_to_stockout'), use_container_width=True)

        st.subheader("⚠️ المنتجات اللي هتخلص")
        # فلترة المنتجات اللي حالتها مش "آمن"
        critical_stock = stock[stock['status'] != "🟢 آمن"]
        st.dataframe(critical_stock, use_container_width=True)

    except Exception as e:
        st.error(f"حصلت مشكلة في قراءة الملف: {e}")
else:
    st.info("يرجى رفع ملف CSV لبدء التحليل.")
