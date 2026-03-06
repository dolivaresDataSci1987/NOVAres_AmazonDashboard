import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Market Structure")

st.caption("Structural composition of the Amazon Beauty market.")

products = pd.read_csv("data/exports/products_final.csv")

price_dist = (
    products
    .groupby("price_range")
    .size()
    .reset_index(name="n_products")
    .sort_values("n_products", ascending=False)
)

review_dist = (
    products
    .groupby("price_range", as_index=False)["review_count"]
    .sum()
    .sort_values("review_count", ascending=False)
)

st.subheader("Price segment structure")

left, right = st.columns(2)

with left:
    fig_products = px.bar(
        price_dist,
        x="price_range",
        y="n_products",
        template="simple_white",
        title="Number of products per price segment"
    )
    st.plotly_chart(fig_products, use_container_width=True)

with right:
    fig_reviews = px.bar(
        review_dist,
        x="price_range",
        y="review_count",
        template="simple_white",
        title="Total reviews per price segment"
    )
    st.plotly_chart(fig_reviews, use_container_width=True)

st.markdown("---")
st.subheader("Brand concentration")

brand_stats = pd.read_csv("data/exports/brand_stats.csv")

top_brands = (
    brand_stats
    .sort_values("total_reviews", ascending=False)
    .head(15)
)

fig_brand_conc = px.bar(
    top_brands,
    x="total_reviews",
    y="brand",
    orientation="h",
    template="simple_white",
    title="Top 15 brands by total reviews"
)

fig_brand_conc.update_layout(yaxis={"categoryorder": "total ascending"})

st.plotly_chart(fig_brand_conc, use_container_width=True)

st.markdown("---")
st.subheader("Cumulative market concentration")

brand_stats = pd.read_csv("data/exports/brand_stats.csv")

concentration = (
    brand_stats[["brand", "total_reviews"]]
    .sort_values("total_reviews", ascending=False)
    .reset_index(drop=True)
)

concentration["rank"] = concentration.index + 1
concentration["cum_reviews"] = concentration["total_reviews"].cumsum()
concentration["cum_share"] = (
    concentration["cum_reviews"] / concentration["total_reviews"].sum()
)

fig_conc = px.line(
    concentration,
    x="rank",
    y="cum_share",
    template="simple_white",
    title="Cumulative share of reviews captured by top brands"
)

fig_conc.update_yaxes(tickformat=".0%")

st.plotly_chart(fig_conc, use_container_width=True)
