# app.py
import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

# Load the dataset
@st.cache_data
def load_data():
    df = pd.read_csv("mutual_funds_india.csv")  # Place the file in the same folder or update the path
    df.columns = df.columns.str.replace(" ", "")
    return df

df = load_data()

st.title("Mutual Funds in India - Return Explorer")

# Category selection
category_options = df.category.unique()
selected_category = st.selectbox("Select a Mutual Fund Category", category_options)

# AMC selection based on category
filtered_df_by_category = df[df.category == selected_category]
amc_options = filtered_df_by_category.AMC_name.unique()
selected_amc = st.selectbox("Select AMC (Fund House)", amc_options)

# Filter by selected AMC
final_df = filtered_df_by_category[filtered_df_by_category.AMC_name == selected_amc]

# Bar plot
st.subheader(f"1-Year Returns for {selected_amc} in {selected_category}")
fig, ax = plt.subplots(figsize=(12, 6))
sb.barplot(x=final_df.MutualFundName, y=final_df.return_1yr, palette='hot', ax=ax)
plt.xticks(rotation=90)
st.pyplot(fig)
