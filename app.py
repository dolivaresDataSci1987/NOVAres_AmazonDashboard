import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="NOVAres | Amazon Beauty Intelligence",
    layout="wide"
)

st.title("NOVAres Amazon Beauty Dashboard")

# Load data
products = pd.read_csv("data/exports/products_final.csv")
brand_stats = pd.read_csv("data/exports/brand_stats.csv")
brand_value = pd.read_csv("data/exports/brand_value.csv")
review_words = pd.read_csv("data/exports/review_word_importance.csv")

st.write("Data loaded successfully")

st.write("Products:", products.shape)
st.write("Brands:", brand_stats.shape)
st.write("Brand value:", brand_value.shape)
st.write("Review words:", review_words.shape)
