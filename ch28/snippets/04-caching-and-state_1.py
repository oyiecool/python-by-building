@st.cache_data(ttl=600)                  # results reused for 10 minutes per distinct argument
def load_orders(path: str) -> pd.DataFrame:
    return pd.read_csv(path, parse_dates=["order_date"])

@st.cache_resource                       # for objects shared by everyone: database connections, ML models
def get_model():
    return joblib.load("model.joblib")
