import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Market Structure")

st.caption("Structural composition of the Amazon Beauty market.")

products = pd.read_csv("data/exports/products_final.csv")

st.subheader("Product distribution by price range")

price_dist = (
    products
    .groupby("price_range")
    .size()
    .reset_index(name="n_products")
    .sort_values("n_products", ascending=False)
)

fig = px.bar(
    price_dist,
    x="price_range",
    y="n_products",
    template="simple_white",
    title="Number of products per price segment"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.subheader("Review volume by price range")

review_dist = (
    products
    .groupby("price_range", as_index=False)["review_count"]
    .sum()
    .sort_values("review_count", ascending=False)
)

fig_reviews = px.bar(
    review_dist,
    x="price_range",
    y="review_count",
    template="simple_white",
    title="Total reviews per price segment"
)

st.plotly_chart(fig_reviews, use_container_width=True)
