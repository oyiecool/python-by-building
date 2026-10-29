import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

# 300 simulated homes: price depends on size, rooms and distance, plus noise
rng = np.random.default_rng(1)
size = rng.uniform(30, 200, 300)                       # m²
rooms = np.clip((size / 30 + rng.normal(0, 0.7, 300)).round(), 1, 7)
dist = rng.uniform(0.5, 25, 300)                       # km to the city centre
price = 40_000 * size + 150_000 * rooms - 60_000 * dist + rng.normal(0, 400_000, 300)

X = np.column_stack([size, rooms, dist])
X_train, X_test, y_train, y_test = train_test_split(X, price, test_size=0.2, random_state=0)

model = LinearRegression().fit(X_train, y_train)
pred = model.predict(X_test)
print(model.coef_.round(0))                     # [ 40043. 137970. -59300.]
print(f"MAE {mean_absolute_error(y_test, pred):,.0f}   R² {r2_score(y_test, pred):.3f}")
print(model.predict([[85, 3, 6]]).round(-3))    # an 85 m², 3-room home 6 km out: [3485000.]
