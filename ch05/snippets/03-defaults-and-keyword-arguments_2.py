def add_item(item, items=None):      # correct pattern
    if items is None:
        items = []
    items.append(item)
    return items
