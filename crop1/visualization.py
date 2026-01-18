import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# ------------------------------
# Load Dataset
# ------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("crop1/crop_yield.csv")  # replace with your dataset

df = load_data()

# ------------------------------
# Page Config
# ------------------------------
st.set_page_config(
    page_title="🌾 फसल उत्पादन भविष्यवाणी (Crop Yield Prediction)",
    page_icon="🌱",
    layout="centered"
)

st.title("🌾 फसल उत्पादन भविष्यवाणी (Crop Yield Prediction)")
st.subheader("📊 डेटा व्हिज्युअलायझेशन")

# ------------------------------
# Dataset Preview
# ------------------------------
if st.checkbox("Show Dataset"):
    st.write(df.head())

# ------------------------------
# Crop Selection
# ------------------------------
if "Crop" in df.columns:
    crop_list = df["Crop"].unique()
    selected_crop = st.selectbox("🌿 फसल निवडा / Select Crop:", crop_list)
    df_crop = df[df["Crop"] == selected_crop]  # filter dataset by selected crop
else:
    df_crop = df

# ------------------------------
# Correlation Heatmap
# ------------------------------
if st.checkbox("Show Correlation Heatmap"):
    st.write(f"📌 Feature Correlation for {selected_crop}")
    plt.figure(figsize=(10,6))
    sns.heatmap(df_crop.corr(numeric_only=True), annot=True, cmap="YlGnBu")
    st.pyplot(plt)
    st.markdown("ℹ️ **This heatmap shows how different factors (rainfall, soil nutrients, temperature, etc.) are related to the yield of the selected crop.** A higher positive value means stronger impact.")

# ------------------------------
# Distribution of Features
# ------------------------------
feature = st.selectbox("Select a feature to visualize:", df.columns)
fig = px.histogram(df_crop, x=feature, nbins=20, title=f"Distribution of {feature} for {selected_crop}")
st.plotly_chart(fig)
st.markdown("ℹ️ **This histogram shows how the values of the selected feature are distributed for the chosen crop.** For example, you can check if rainfall or yield is usually high or low.")

# ------------------------------
# Yield Distribution (Box Plot)
# ------------------------------
fig2 = px.box(df_crop, y="Yield", color="Crop",
              title=f"🌱 Yield Distribution for {selected_crop}")
st.plotly_chart(fig2)
st.markdown("ℹ️ **This box plot shows how the yield values vary for the selected crop.** The box shows the middle range, while points outside show unusual high or low yields.")

# ------------------------------
# Average Yield by State (Bar Chart)
# ------------------------------
if "State" in df_crop.columns:
    avg_state_yield = df_crop.groupby("State")["Yield"].mean().reset_index().sort_values(by="Yield", ascending=False)
    fig3 = px.bar(avg_state_yield, x="State", y="Yield", color="State",
                  title=f"🏆 State-wise Average Yield for {selected_crop}")
    st.plotly_chart(fig3)
    st.markdown("ℹ️ **This bar chart shows the average yield of the selected crop in each state.** Higher bars indicate states where the crop performs better.")

# ------------------------------
# Yield vs Rainfall (Scatter + Trendline)
# ------------------------------
if "Rainfall" in df_crop.columns and "Yield" in df_crop.columns:
    fig4 = px.scatter(df_crop, x="Rainfall", y="Yield", color="State",
                      trendline="ols", title=f"🌧️ Rainfall vs Yield for {selected_crop}")
    st.plotly_chart(fig4)
    st.markdown("ℹ️ **This scatter plot shows how rainfall affects the yield of the crop.** The line shows the trend: upward means more rainfall improves yield, downward means the opposite.")

# ------------------------------
# Season-wise Yield
# ------------------------------
if "Season" in df_crop.columns:
    fig5 = px.box(df_crop, x="Season", y="Yield", color="Season",
                  title=f"🌤️ Season-wise Yield for {selected_crop}")
    st.plotly_chart(fig5)
    st.markdown("ℹ️ **This chart shows the yield distribution of the selected crop across different seasons (Kharif, Rabi, etc.).** It helps understand which season is most suitable for the crop.")

# ------------------------------
# Top 10 States for Selected Crop
# ------------------------------
if "State" in df_crop.columns:
    top_states = avg_state_yield.head(10)
    fig6 = px.bar(top_states, x="State", y="Yield", color="State",
                  title=f"🏆 Top 10 States by Yield for {selected_crop}")
    st.plotly_chart(fig6)
    st.markdown("ℹ️ **This chart shows the top 10 states with the highest average yield for the selected crop.** It highlights the best-performing regions.")

# ------------------------------
# Pairplot (Numeric Features)
# ------------------------------
if st.checkbox("Show Pairplot (All Numeric Features)"):
    st.write(f"📌 Pairplot for {selected_crop}")
    fig7 = sns.pairplot(df_crop.select_dtypes(include="number"), diag_kind="kde")
    st.pyplot(fig7)
    st.markdown("ℹ️ **This pairplot shows relationships between all numeric features (like Rainfall, Temperature, Yield).** It helps find hidden patterns and correlations.")
