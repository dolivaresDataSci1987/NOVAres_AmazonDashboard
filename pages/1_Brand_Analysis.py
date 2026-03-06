import streamlit as st
import pandas as pd
import plotly.express as px


st.title("Brand Analysis")
st.caption("Brand-level analysis of scale, pricing, catalog mix, product performance, and perception proxies.")


@st.cache_data
def load_data():
    products = pd.read_csv("data/exports/products_final.csv")
    brand_stats = pd.read_csv("data/exports/brand_stats.csv")
    brand_value = pd.read_csv("data/exports/brand_value.csv")
    review_words = pd.read_csv("data/exports/review_word_importance.csv")
    return products, brand_stats, brand_value, review_words


products, brand_stats, brand_value, review_words = load_data()

# Basic cleaning
products = products.copy()
products["brand"] = products["brand"].astype(str).str.strip()
brand_stats["brand"] = brand_stats["brand"].astype(str).str.strip()
brand_value["brand"] = brand_value["brand"].astype(str).str.strip()

products = products.dropna(subset=["brand", "price", "avg_rating", "review_count"])
brand_stats = brand_stats.dropna(subset=["brand"])
brand_value = brand_value.dropna(subset=["brand", "avg_price", "avg_rating", "value_score"])

products = products[products["brand"] != ""]
brand_stats = brand_stats[brand_stats["brand"] != ""]
brand_value = brand_value[brand_value["brand"] != ""]


# --------------------------------------------------
# Section 1: Top brands by total reviews
# --------------------------------------------------
st.markdown("---")
st.subheader("Top brands by total reviews")

top_review_brands = (
    brand_stats
    .sort_values("total_reviews", ascending=False)
    .head(15)
)

fig_reviews = px.bar(
    top_review_brands,
    x="total_reviews",
    y="brand",
    orientation="h",
    template="simple_white",
    title="Top 15 brands by total reviews"
)
fig_reviews.update_layout(yaxis={"categoryorder": "total ascending"})

st.plotly_chart(fig_reviews, use_container_width=True)


# --------------------------------------------------
# Section 2: Top brands by average price
# --------------------------------------------------
st.markdown("---")
st.subheader("Top brands by average price")

price_brands = (
    brand_value
    .merge(
        brand_stats[["brand", "total_reviews"]],
        on="brand",
        how="left"
    )
    .copy()
)

# avoid very noisy brands with too few products
price_brands = price_brands[price_brands["n_products"] >= 3]

top_price_brands = (
    price_brands
    .sort_values("avg_price", ascending=False)
    .head(15)
)

fig_price = px.bar(
    top_price_brands,
    x="avg_price",
    y="brand",
    orientation="h",
    template="simple_white",
    title="Top 15 brands by average price (min. 3 products)"
)
fig_price.update_layout(yaxis={"categoryorder": "total ascending"})

st.plotly_chart(fig_price, use_container_width=True)


# --------------------------------------------------
# Section 3: Price range mix by selected brand
# --------------------------------------------------
st.markdown("---")
st.subheader("Price range mix by selected brand")

available_brands = sorted(products["brand"].dropna().unique().tolist())

selected_brand = st.selectbox(
    "Select a brand",
    options=available_brands
)

brand_products = products[products["brand"] == selected_brand].copy()

price_mix = (
    brand_products
    .groupby("price_range")
    .size()
    .reset_index(name="n_products")
    .sort_values("n_products", ascending=False)
)

left, right = st.columns([1.2, 1])

with left:
    fig_mix = px.bar(
        price_mix,
        x="price_range",
        y="n_products",
        template="simple_white",
        title=f"{selected_brand} — product mix by price range"
    )
    st.plotly_chart(fig_mix, use_container_width=True)

with right:
    st.write("Brand summary")
    st.dataframe(
        pd.DataFrame({
            "Metric": [
                "Products",
                "Average price",
                "Average rating",
                "Total reviews"
            ],
            "Value": [
                f"{brand_products.shape[0]:,}",
                f"${brand_products['price'].mean():.2f}",
                f"{brand_products['avg_rating'].mean():.2f}",
                f"{brand_products['review_count'].sum():,}"
            ]
        }),
        use_container_width=True,
        hide_index=True
    )


# --------------------------------------------------
# Section 4: Top products for selected brand
# --------------------------------------------------
st.markdown("---")
st.subheader("Top products for selected brand")

metric_choice = st.radio(
    "Rank products by",
    options=["review_count", "avg_rating", "rating_residual"],
    horizontal=True
)

top_products = (
    brand_products
    .sort_values(metric_choice, ascending=False)
    .head(15)
    [["parent_asin", "price", "avg_rating", "review_count", "rating_residual", "price_range"]]
    .copy()
)

top_products = top_products.rename(columns={
    "parent_asin": "ASIN",
    "price": "Price",
    "avg_rating": "Avg Rating",
    "review_count": "Reviews",
    "rating_residual": "Rating Residual",
    "price_range": "Price Range"
})

st.dataframe(top_products, use_container_width=True, hide_index=True)


# --------------------------------------------------
# Section 5: Brand perception proxy
# --------------------------------------------------
st.markdown("---")
st.subheader("Brand perception proxy")

brand_residual = (
    products
    .groupby("brand", as_index=False)
    .agg(
        avg_brand_rating=("avg_rating", "mean"),
        avg_brand_residual=("rating_residual", "mean"),
        total_reviews=("review_count", "sum"),
        n_products=("parent_asin", "count")
    )
)

brand_residual = brand_residual[brand_residual["n_products"] >= 3]

c1, c2 = st.columns(2)

with c1:
    top_rated = (
        brand_residual
        .sort_values("avg_brand_rating", ascending=False)
        .head(15)
    )

    fig_top_rated = px.bar(
        top_rated,
        x="avg_brand_rating",
        y="brand",
        orientation="h",
        template="simple_white",
        title="Top brands by average rating (min. 3 products)"
    )
    fig_top_rated.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_top_rated, use_container_width=True)

with c2:
    top_residual = (
        brand_residual
        .sort_values("avg_brand_residual", ascending=False)
        .head(15)
    )

    fig_top_residual = px.bar(
        top_residual,
        x="avg_brand_residual",
        y="brand",
        orientation="h",
        template="simple_white",
        title="Top brands by average rating residual (min. 3 products)"
    )
    fig_top_residual.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_top_residual, use_container_width=True)
