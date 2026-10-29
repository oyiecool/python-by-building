import re
from collections import Counter

text = "The cat and the hat. The bat sat on the mat, and the cat ran!"
words = re.findall(r"[a-z']+", text.lower())
print(Counter(words).most_common(5))
# [('the', 5), ('cat', 2), ('and', 2), ('hat', 1), ('bat', 1)]
