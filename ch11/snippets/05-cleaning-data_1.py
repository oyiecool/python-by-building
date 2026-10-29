raw = pd.DataFrame({
    "name": [" Ana ", "BEN", "cara", None, "Ana"],
    "age": ["31", "n/a", "27", "45", "31"],
    "city": ["Manila", "cebu", "Davao", "Manila", "Manila"],
})

df = raw.copy()
df["name"] = df["name"].str.strip().str.title()
df["city"] = df["city"].str.title()
df["age"] = pd.to_numeric(df["age"], errors="coerce")   # "n/a" -> NaN
print(df.isna().sum())                                    # missing per column
df = df.dropna(subset=["name"])                           # drop rows with no name
df["age"] = df["age"].fillna(df["age"].median())
df = df.drop_duplicates()
print(df)
