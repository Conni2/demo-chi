import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import os

# Load your dataset (replace with your own CSV or use mock dataframe)
df = pd.read_csv("claims_dataset.csv")  # Replace with your actual file

st.set_page_config(page_title="Cosmetic Claim Map", layout="wide")
st.title("🧴 Cosmetic Claim Mapping Dashboard")

# Sidebar Filters
st.sidebar.header("Filter")
selected_country = st.sidebar.selectbox("Country", sorted(df["country"].unique()))
filtered_df = df[df["country"] == selected_country]

selected_products = st.sidebar.multiselect("Select Products", options=sorted(filtered_df["product_name"].unique()), default=sorted(filtered_df["product_name"].unique()))
filtered_df = filtered_df[filtered_df["product_name"].isin(selected_products)]

selected_touchpoints = st.sidebar.multiselect("Touchpoints", options=sorted(df["touchpoint"].unique()), default=sorted(df["touchpoint"].unique()))
filtered_df = filtered_df[filtered_df["touchpoint"].isin(selected_touchpoints)]

menu = st.sidebar.radio("Select View", ["Product Mapping", "Competitor Claim Map"])

if menu == "Product Mapping":
    st.header("📌 Product Claim Mapping")
    selected_brand = st.selectbox("Select Brand", sorted(filtered_df["brand"].unique()))
    selected_product = st.selectbox("Select Product", sorted(filtered_df["product_name"].unique()))

    # Compose image path
    image_filename = f"images/{selected_country}_{selected_brand}_{selected_product}.png"

    if os.path.exists(image_filename):
        st.image(Image.open(image_filename), caption=f"Claim Mapping: {selected_product}", use_column_width=True)
    else:
        st.warning("No image available for selected filters.")

else:
    st.header("📊 Competitor Claim Map")
    st.subheader(f"Country: {selected_country}")

    fig = px.scatter(
        filtered_df,
        x="x_category",
        y="claim_type",
        size="relevancy",
        color="product_name",
        hover_data=["claim_text", "touchpoint"],
        opacity=0.7,
        height=700,
    )

    st.plotly_chart(fig, use_container_width=True)

    # Export to image button
    img_bytes = fig.to_image(format="png", width=1280, height=720, scale=2)
    st.download_button(
        label="📥 Download 16:9 Graph Image",
        data=img_bytes,
        file_name="claim_map.png",
        mime="image/png"
    )
