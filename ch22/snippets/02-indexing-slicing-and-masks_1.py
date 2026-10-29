m = np.arange(1, 13).reshape(3, 4)
# [[ 1  2  3  4]
#  [ 5  6  7  8]
#  [ 9 10 11 12]]
m[0, 2]          # 3          row 0, column 2
m[1]             # [5 6 7 8]  one row
m[:, 1]          # [ 2  6 10] one column
m[:2, 2:]        # [[3 4] [7 8]]

temps = np.array([29.5, 31.2, 33.8, 28.1, 35.0, 30.4])
hot = temps > 32                     # boolean mask: [F F T F T F]
print(temps[hot])                    # [33.8 35. ]
print(hot.sum(), hot.mean())         # 2 hot days, 33% of days
temps[temps > 34] = 34               # cap values in place
print(np.where(temps > 30, "warm", "mild"))
