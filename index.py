import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Universal Data Visualizer", page_icon="📊", layout="wide")

# Streamlit App
st.title("📊 Universal Data Visualizer")
st.write("Upload any dataset and explore different visualizations.")

# File uploader
df = st.file_uploader("📂 Upload dataset (CSV or XLSX)", type=['csv', 'xlsx'])

# Function to visualize data
def visualize_data(data, chart_type, x_axis, y_axis, color_col):
    st.write(f"## 📈 {chart_type.capitalize()} Chart")

    if chart_type == "bar":
        fig = px.bar(data, x=x_axis, y=y_axis, color=color_col, text=y_axis, barmode="group")
    elif chart_type == "line":
        fig = px.line(data, x=x_axis, y=y_axis, color=color_col, markers=True)
    elif chart_type == "scatter":
        fig = px.scatter(data, x=x_axis, y=y_axis, color=color_col, size=y_axis, hover_data=data.columns)
    elif chart_type == "pie":
        fig = px.pie(data, names=x_axis, values=y_axis, color=color_col, hole=0.3)
    elif chart_type == "histogram":
        fig = px.histogram(data, x=x_axis, y=y_axis, color=color_col, marginal="rug")

    # Display chart
    st.plotly_chart(fig, use_container_width=True)

# Load & display data
if df is not None:
    if df.name.endswith('.csv'):
        data = pd.read_csv(df)
    elif df.name.endswith('.xlsx'):
        data = pd.read_excel(df)
    else:
        st.error('🚨 Please upload a valid CSV or XLSX file.')
        st.stop()

    # Ensure the "Date" column (if present) is in the correct format
    for col in data.columns:
        if "date" in col.lower():
            data[col] = pd.to_datetime(data[col])

    # Display dataset
    st.write("### 📝 Uploaded Dataset")
    st.dataframe(data)

    # User selects columns for visualization
    numeric_columns = data.select_dtypes(include=['number']).columns.tolist()
    categorical_columns = data.select_dtypes(include=['object', 'category']).columns.tolist()

    if numeric_columns and categorical_columns:
        chart_type = st.selectbox("📊 Select Chart Type", ["bar", "line", "scatter", "pie", "histogram"])
        x_axis = st.selectbox("📅 Select X-axis", data.columns)
        y_axis = st.selectbox("🔢 Select Y-axis", numeric_columns)
        color_col = st.selectbox("🎨 Select Color Grouping (Optional)", ["None"] + categorical_columns)

        if color_col == "None":
            color_col = None

        # Visualize button
        if st.button("🔍 Visualize Data"):
            visualize_data(data, chart_type, x_axis, y_axis, color_col)
    else:
        st.warning("🚨 Dataset must contain at least one numeric and one categorical column for visualization.")
else:
    st.warning("📂 Please upload a file to proceed.")
