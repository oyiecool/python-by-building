fruits.append("date")          # add to end
fruits.insert(1, "avocado")    # insert at position 1
fruits.extend(["fig", "grape"])# add several
fruits.remove("banana")        # remove first match
last = fruits.pop()            # remove and return last
first = fruits.pop(0)          # remove and return index 0
fruits[0] = "apricot"          # replace
del fruits[1]                  # delete by index
