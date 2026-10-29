from fastapi import HTTPException, status

class ItemOut(BaseModel):
    id: int
    name: str

@app.get("/items/{item_id}", response_model=ItemOut)
def read_item(item_id: int):
    item = ITEMS.get(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item not found")
    return item            # extra fields (like a password hash) are stripped by response_model
