# dashboard.py - Chapter 28 mini project
"""Interactive sales dashboard: filters in the sidebar, KPI cards, charts and a downloadable table.
Run with:  streamlit run dashboard.py"""
from pathlib import Path

import pandas as pd
import streamlit as st

DATA = Path(__file__).resolve().parent / "orders.csv"      # from Chapter 11

st.set_page_config(page_title="Sales dashboard", layout="wide")


@st.cache_data                                  # read and prepare once, not on every click
def load(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["order_date"])
    df["revenue"] = df["units"] * df["unit_price"]
    df["month"] = df["order_date"].dt.to_period("M").dt.to_timestamp()
    return df


df = load(DATA)

st.sidebar.header("Filters")
regions = st.sidebar.multiselect("Region", sorted(df["region"].unique()), default=sorted(df["region"].unique()))
products = st.sidebar.multiselect("Product", sorted(df["product"].unique()), default=sorted(df["product"].unique()))
start, end = st.sidebar.date_input("Date range", (df["order_date"].min().date(), df["order_date"].max().date()))
target = st.sidebar.number_input("Monthly revenue target", min_value=0, value=15_000_000, step=500_000)

view = df[df["region"].isin(regions) & df["product"].isin(products)
          & df["order_date"].between(pd.Timestamp(start), pd.Timestamp(end))]

st.title("Sales dashboard")
st.caption(f"{len(view):,} of {len(df):,} orders match the filters")

if view.empty:
    st.warning("No orders match these filters.")
    st.stop()

monthly = view.groupby("month")["revenue"].sum()
c1, c2, c3, c4 = st.columns(4)
c1.metric("Revenue", f"{view['revenue'].sum() / 1e6:,.1f} M")
c2.metric("Orders", f"{len(view):,}")
c3.metric("Average order", f"{view['revenue'].mean():,.0f}")
if len(monthly) >= 2:
    change = monthly.iloc[-1] / monthly.iloc[-2] - 1
    c4.metric("Last month", f"{monthly.iloc[-1] / 1e6:,.1f} M", f"{change:+.1%}")
months_on_target = int((monthly >= target).sum())
st.progress(months_on_target / len(monthly), text=f"{months_on_target} of {len(monthly)} months reached the target")

left, right = st.columns(2)
with left:
    st.subheader("Revenue by month (millions)")
    st.line_chart((monthly / 1e6).rename("revenue"))
with right:
    st.subheader("Revenue by region (millions)")
    st.bar_chart(view.groupby("region")["revenue"].sum().div(1e6).sort_values(ascending=False))

st.subheader("Top sales reps")
reps = (view.groupby("rep").agg(orders=("revenue", "size"), revenue=("revenue", "sum"))
            .sort_values("revenue", ascending=False))
reps["share"] = reps["revenue"] / reps["revenue"].sum()
st.dataframe(reps.style.format({"revenue": "{:,.0f}", "share": "{:.0%}"}), width="stretch")

st.download_button("Download filtered orders (CSV)", view.to_csv(index=False).encode("utf-8"),
                   file_name="filtered_orders.csv", mime="text/csv")
