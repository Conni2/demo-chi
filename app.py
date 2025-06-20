import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import os
import plotly.io as pio

# Load dataset
df = pd.read_csv("claims_dataset.csv")

st.set_page_config(page_title="Cosmetic Claim Mapping", layout="wide")
st.title("🧴 Cosmetic Claim Mapping Dashboard")

# Sidebar View Selector
st.sidebar.header("Navigation")
menu = st.sidebar.radio("Select View", ["Product Mapping", "Competitor Claim Map"])

if menu == "Product Mapping":
    st.header("📌 Product Claim Mapping")

    # Filters (top of the page)
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_country = st.selectbox("Select Country", sorted(df["country"].unique()))
    with col2:
        selected_brand = st.selectbox("Select Brand", sorted(df[df["country"] == selected_country]["brand"].unique()))
    with col3:
        selected_product = st.selectbox("Select Product", sorted(df[(df["country"] == selected_country) & (df["brand"] == selected_brand)]["product_name"].unique()))

    # Compose image path
    image_filename = f"images/{selected_country}_{selected_brand}_{selected_product}.png"

    if os.path.exists(image_filename):
        st.image(Image.open(image_filename), caption=f"Claim Mapping: {selected_product}", use_column_width=True)
    else:
        st.warning("No image available for selected filters.")

else:
    st.header("📊 Competitor Claim Map")

    # Filters (top of the page)
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_country = st.selectbox("Select Country", sorted(df["country"].unique()))
    with col2:
        selected_products = st.multiselect("Select Products", sorted(df[df["country"] == selected_country]["product_name"].unique()))
    with col3:
        selected_touchpoints = st.multiselect("Select Touchpoints", sorted(df["touchpoint"].unique()), default=sorted(df["touchpoint"].unique()))

    # Filter dataframe
    filtered_df = df[(df["country"] == selected_country) & 
                     (df["product_name"].isin(selected_products)) & 
                     (df["touchpoint"].isin(selected_touchpoints))]

    # Define custom x-axis category order matching the image reference
    x_category_order = [
    "science/formulation/ingredient/packaging",
    "emotion",
    "sensory",
    "consumer perception",
    "clinical/instrumental",
    "local relevance/safety/sustainability",
    "shares/sales/R&R/endorsement"
]

    fig = px.strip(
        filtered_df,
        x="x_category",
        y="claim_type",
        category_orders={"x_category": x_category_order},
        color="product_name",
        hover_data=["claim_text", "touchpoint"],
        stripmode="overlay",
        labels={"x_category": "", "claim_type": ""},
        height=1000  # Increase vertical space for more y-axis spreading
    )

    fig.update_traces(jitter=0.6, marker=dict(size=14, opacity=0.7))
fig.update_layout(yaxis=dict(tickmode='array', tickvals=['statement', 'imagery', 'comparative/superiority'], tickangle=0, tickfont=dict(size=14)))
    st.plotly_chart(fig, use_container_width=True)

    # Safe image export block
    try:
        img_bytes = fig.to_image(format="png", width=1280, height=720, scale=2)
        st.download_button(
            label="📥 Download 16:9 Graph Image",
            data=img_bytes,
            file_name="claim_map.png",
            mime="image/png"
        )
    except Exception:
        st.info("❌ Image download is currently not supported in this environment. If you're running this locally, it will work. Try installing Kaleido with \"pip install -U kaleido\".")
