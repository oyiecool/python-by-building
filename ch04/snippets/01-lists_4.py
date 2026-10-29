scores = [72, 95, 88, 61, 95]
print(95 in scores)            # True
print(scores.index(88))        # 2
print(scores.count(95))        # 2
print(sum(scores), min(scores), max(scores))
print(sorted(scores))          # new sorted list
scores.sort(reverse=True)      # sorts in place
