import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("Market Structure")

st.caption("Structural analysis of the Amazon Beauty market.")

products = pd.read_csv("data/exports/products_final.csv")

st.write("Total products:", products.shape[0])
