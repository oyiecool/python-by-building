choice = st.radio("View", ["Monthly", "Weekly"], horizontal=True)
regions = st.multiselect("Regions", ["NCR", "Luzon", "Visayas", "Mindanao"], default=["NCR"])
show_raw = st.checkbox("Show raw data")
upload = st.file_uploader("Upload a CSV", type="csv")
if upload is not None:
    df = pd.read_csv(upload)

left, right = st.columns([2, 1])         # 2:1 width
with left:
    st.line_chart(data)
with right:
    st.metric("Total", total)

tab1, tab2 = st.tabs(["Charts", "Data"])
with tab1:
    st.bar_chart(data)
with tab2:
    st.dataframe(data)

st.sidebar.header("Filters")              # anything on st.sidebar goes in the left panel
