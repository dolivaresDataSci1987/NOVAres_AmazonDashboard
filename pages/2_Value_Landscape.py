import streamlit as st
import pandas as pd
import plotly.express as px


st.title("Value Landscape")
st.caption("Market-level view of perceived value across price segments and relative product performance.")


@st.cache_data
def load_data():
    products = pd.read_csv("data/exports/products_final.csv")
    return products


products = load_data().copy()

products["price_range"] = products["price_range"].astype(str).str.strip()
products = products.dropna(subset=["price_range", "avg_rating", "rating_residual"])
products = products[products["price_range"] != ""]


rating_by_price = (
    products
    .groupby("price_range", as_index=False)
    .agg(avg_rating=("avg_rating", "mean"))
    .sort_values("avg_rating", ascending=False)
)

residual_by_price = (
    products
    .groupby("price_range", as_index=False)
    .agg(avg_residual=("rating_residual", "mean"))
    .sort_values("avg_residual", ascending=False)
)

st.markdown("---")
st.subheader("Value by price segment")

left, right = st.columns(2)

with left:
    fig_rating = px.bar(
        rating_by_price,
        x="price_range",
        y="avg_rating",
        template="simple_white",
        title="Average rating by price range"
    )
    st.plotly_chart(fig_rating, use_container_width=True)

with right:
    fig_residual = px.bar(
        residual_by_price,
        x="price_range",
        y="avg_residual",
        template="simple_white",
        title="Average rating residual by price range"
    )
    st.plotly_chart(fig_residual, use_container_width=True)

st.markdown("---")
st.subheader("Heatmap: price range × review bucket")

heatmap_df = (
    products
    .dropna(subset=["review_bucket"])
    .groupby(["price_range", "review_bucket"], as_index=False)
    .agg(
        avg_rating=("avg_rating", "mean"),
        avg_residual=("rating_residual", "mean"),
        n_products=("parent_asin", "count")
    )
)

metric_option = st.radio(
    "Heatmap metric",
    options=["avg_rating", "avg_residual", "n_products"],
    horizontal=True
)

metric_titles = {
    "avg_rating": "Average rating",
    "avg_residual": "Average rating residual",
    "n_products": "Number of products"
}

fig_heatmap = px.density_heatmap(
    heatmap_df,
    x="review_bucket",
    y="price_range",
    z=metric_option,
    text_auto=".2f" if metric_option != "n_products" else True,
    template="simple_white",
    title=f"Heatmap of {metric_titles[metric_option]} by price range and review bucket"
)

st.plotly_chart(fig_heatmap, use_container_width=True)

st.markdown("---")
st.subheader("Top overperformers / underperformers")

min_reviews = st.slider(
    "Minimum reviews for product ranking",
    min_value=0,
    max_value=int(products["review_count"].max()),
    value=20
)

eligible_products = products[products["review_count"] >= min_reviews].copy()

top_overperformers = (
    eligible_products
    .sort_values("rating_residual", ascending=False)
    .head(15)
    [["parent_asin", "brand", "price", "avg_rating", "review_count", "rating_residual", "price_range"]]
    .rename(columns={
        "parent_asin": "ASIN",
        "brand": "Brand",
        "price": "Price",
        "avg_rating": "Avg Rating",
        "review_count": "Reviews",
        "rating_residual": "Rating Residual",
        "price_range": "Price Range"
    })
)

top_underperformers = (
    eligible_products
    .sort_values("rating_residual", ascending=True)
    .head(15)
    [["parent_asin", "brand", "price", "avg_rating", "review_count", "rating_residual", "price_range"]]
    .rename(columns={
        "parent_asin": "ASIN",
        "brand": "Brand",
        "price": "Price",
        "avg_rating": "Avg Rating",
        "review_count": "Reviews",
        "rating_residual": "Rating Residual",
        "price_range": "Price Range"
    })
)

left, right = st.columns(2)

with left:
    st.write("Top overperformers")
    st.dataframe(top_overperformers, use_container_width=True, hide_index=True)

with right:
    st.write("Top underperformers")
    st.dataframe(top_underperformers, use_container_width=True, hide_index=True)
