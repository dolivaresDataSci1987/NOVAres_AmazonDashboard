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
