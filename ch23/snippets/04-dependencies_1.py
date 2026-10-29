from fastapi import Depends, Header

def require_api_key(x_api_key: str = Header()):
    if x_api_key != os.environ.get("API_KEY", "dev-key"):
        raise HTTPException(status_code=401, detail="invalid API key")

@app.delete("/items/{item_id}", dependencies=[Depends(require_api_key)], status_code=204)
def delete_item(item_id: int):
    ITEMS.pop(item_id, None)
