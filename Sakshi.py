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

df = load_data()

st.set_page_config(page_title="Mutual Funds Explorer", layout="wide")

st.title("📈 Mutual Funds in India - Return Explorer")

# Sidebar filters
st.sidebar.header("🔍 Filter Funds")

# Category filter
category_options = df.category.unique()
selected_category = st.sidebar.selectbox("Select Fund Category", sorted(category_options))

filtered_by_category = df[df.category == selected_category]

# AMC filter
amc_options = filtered_by_category.AMC_name.unique()
selected_amc = st.sidebar.selectbox("Select AMC", sorted(amc_options))

filtered_by_amc = filtered_by_category[filtered_by_category.AMC_name == selected_amc]

# Minimum 1-year return filter
min_return = st.sidebar.slider("Minimum 1-Year Return (%)", 
                               min_value=float(df.return_1yr.min()), 
                               max_value=float(df.return_1yr.max()), 
                               value=float(df.return_1yr.min()))
filtered_by_return = filtered_by_amc[filtered_by_amc.return_1yr >= min_return]

# Search by Mutual Fund name
search_term = st.sidebar.text_input("🔎 Search Mutual Fund Name (Optional)").lower()

if search_term:
    final_df = filtered_by_return[filtered_by_return.MutualFundName.str.lower().str.contains(search_term)]
else:
    final_df = filtered_by_return

# Sort results
sort_order = st.sidebar.radio("Sort by Return", ["Descending", "Ascending"])
final_df = final_df.sort_values(by="return_1yr", ascending=(sort_order == "Ascending"))

# Display number of results
st.markdown(f"### Showing {len(final_df)} mutual funds for **{selected_amc}** under **{selected_category}**")

# Interactive plot
if not final_df.empty:
    fig = px.bar(final_df,
                 x='MutualFundName',
                 y='return_1yr',
                 color='return_1yr',
                 color_continuous_scale='RdYlGn',
                 labels={'return_1yr': '1-Year Return (%)'},
                 title=f"1-Year Returns for {selected_amc} - {selected_category}")

    fig.update_layout(xaxis_tickangle=-45,
                      xaxis_title="Mutual Fund",
                      yaxis_title="Return (%)",
                      height=600)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No mutual funds match the selected criteria.")

# Optional: Show data table
with st.expander("📊 Show Data Table"):
    st.dataframe(final_df.reset_index(drop=True))
