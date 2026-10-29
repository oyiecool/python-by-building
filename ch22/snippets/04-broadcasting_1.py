sales = np.array([[120, 80, 45],      # rows = stores, columns = products
                  [200, 95, 60],
                  [ 90, 40, 30]])
price = np.array([45.0, 18.0, 22.0])  # one price per product, shape (3,)
revenue = sales * price               # each row multiplied by the price row
print(revenue.sum(axis=1))            # revenue per store

# standardize each column: subtract its mean, divide by its standard deviation
z = (sales - sales.mean(axis=0)) / sales.std(axis=0)
