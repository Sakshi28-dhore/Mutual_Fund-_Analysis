# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
@st.cache_data
def load_data():
    df = pd.read_csv("mutual_funds_india.csv")
    df.columns = df.columns.str.replace(" ", "")
    return df

# Load data
df = load_data()

# Page configuration
st.set_page_config(page_title="Mutual Funds Explorer", layout="wide")

# Title
st.title("📊 Mutual Funds in India - Return Explorer")

# Sidebar - Filters
st.sidebar.header("🔍 Filter Options")

# Category Filter
category_options = df.category.dropna().unique()
selected_category = st.sidebar.selectbox("Select Fund Category", sorted(category_options))

# Filter based on category
filtered_category_df = df[df.category == selected_category]

# AMC Filter
amc_options = filtered_category_df.AMC_name.dropna().unique()
selected_amc = st.sidebar.selectbox("Select AMC (Fund House)", sorted(amc_options))

# Filter based on AMC
filtered_amc_df = filtered_category_df[filtered_category_df.AMC_name == selected_amc]

# Slider - 1-Year Return Filter
min_return = float(filtered_amc_df.return_1yr.min())
max_return = float(filtered_amc_df.return_1yr.max())
return_range = st.sidebar.slider("Filter by 1-Year Return (%)", min_value=min_return, max_value=max_return, value=(min_return, max_return))
filtered_return_df = filtered_amc_df[(filtered_amc_df.return_1yr >= return_range[0]) & (filtered_amc_df.return_1yr <= return_range[1])]

# Search Mutual Fund Name
search_query = st.sidebar.text_input("Search Mutual Fund Name").lower()
if search_query:
    filtered_final_df = filtered_return_df[filtered_return_df.MutualFundName.str.lower().str.contains(search_query)]
else:
    filtered_final_df = filtered_return_df

# Sorting
sort_order = st.sidebar.radio("Sort by 1-Year Return", options=["Descending", "Ascending"])
filtered_final_df = filtered_final_df.sort_values(by="return_1yr", ascending=(sort_order == "Ascending"))

# Display result count
st.markdown(f"### 🎯 {len(filtered_final_df)} Funds found in **{selected_amc}** - **{selected_category}**")

# Plotly Bar Chart
if not filtered_final_df.empty:
    fig = px.bar(filtered_final_df,
                 x="MutualFundName",
                 y="return_1yr",
                 color="return_1yr",
                 color_continuous_scale="RdYlGn",
                 title=f"1-Year Returns of Funds under {selected_amc}",
                 labels={"return_1yr": "1-Year Return (%)"})
    
    fig.update_layout(xaxis_tickangle=-45, height=600)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No mutual funds found with the selected filters.")

# Show raw data
with st.expander("📄 Show Data Table"):
    st.dataframe(filtered_final_df.reset_index(drop=True))
