import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="NOVAres | Amazon Beauty Intelligence",
    layout="wide"
)

# Load data
products = pd.read_csv("data/exports/products_final.csv")
brand_stats = pd.read_csv("data/exports/brand_stats.csv")
brand_value = pd.read_csv("data/exports/brand_value.csv")
review_words = pd.read_csv("data/exports/review_word_importance.csv")

st.title("NOVAres | Amazon Beauty Market Intelligence")
st.caption("Executive dashboard for Amazon Beauty market structure, brand competition, value, and review signals.")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Products", f"{products.shape[0]:,}")

with col2:
    st.metric("Brands", f"{brand_stats.shape[0]:,}")

with col3:
    st.metric("Brand Value Rows", f"{brand_value.shape[0]:,}")

with col4:
    st.metric("Review Terms", f"{review_words.shape[0]:,}")

st.markdown("---")

st.subheader("Market snapshot")

left, right = st.columns(2)

with left:
    price_chart = px.histogram(
        products[products["price"] < 200],
        x="price",
        nbins=40,
        template="simple_white",
        title="Price Distribution (< $200)"
    )
    st.plotly_chart(price_chart, use_container_width=True)

with right:
    rating_chart = px.histogram(
        products,
        x="avg_rating",
        nbins=30,
        template="simple_white",
        title="Rating Distribution"
    )
    st.plotly_chart(rating_chart, use_container_width=True)

st.markdown("---")
st.subheader("Top brands by review volume")

top_brands = (
    brand_stats
    .sort_values("total_reviews", ascending=False)
    .head(15)
)

fig = px.bar(
    top_brands,
    x="total_reviews",
    y="brand",
    orientation="h",
    template="simple_white",
    title="Top 15 Brands by Total Reviews"
)

fig.update_layout(yaxis={'categoryorder':'total ascending'})

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.subheader("Brand positioning map")

fig_comp = px.scatter(
    brand_stats,
    x="avg_rating",
    y="avg_price",
    size="total_reviews",
    hover_name="brand",
    template="simple_white",
    title="Brand Positioning: Rating vs Price"
)

st.plotly_chart(fig_comp, use_container_width=True)
