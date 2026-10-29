class Stack:
    def __init__(self): self._items = []
    def push(self, x): self._items.append(x)
    def pop(self): return self._items.pop()
    def peek(self): return self._items[-1]
    def is_empty(self): return not self._items
    def __len__(self): return len(self._items)

def balanced(s: str) -> bool:
    pairs, st = {")": "(", "]": "[", "}": "{"}, Stack()
    for ch in s:
        if ch in "([{":
            st.push(ch)
        elif ch in pairs:
            if st.is_empty() or st.pop() != pairs[ch]:
                return False
    return st.is_empty()

print(balanced("{[()]}"), balanced("{[(])}"), balanced("(("))   # True False False
