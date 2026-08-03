import uuid
from fastapi import APIRouter, HTTPException, status
from backend.app.schemas import ItemCreate, ItemStatus, ItemUpdate, ItemOut, ItemUpdate
from backend.app.storage import load_data, save_data

router = APIRouter(prefix="/api/v1/items", tags=["items"])

items = [
    {"id": 1, "name": "Foo"},
    {"id": 2, "name": "Bar"},
    {"id": 3, "name": "Baz"},
]


@router.get("/", response_model=list[ItemOut])
def get_items():
    """Retrieve all items."""
    items = load_data()
    return items


@router.post("/", response_model=ItemOut, status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemCreate):
    """Create a new item."""
    items = load_data()
    new_item = {
        "id": str(uuid.uuid4()),
        "title": payload.title,
        "description": payload.description,
        "priority": payload.priority,
        "status": ItemStatus.OPEN,
    }
    items.append(new_item)
    save_data(items)
    return new_item



@router.get("/{item_id}", response_model=ItemOut)
def get_item(item_id: str):
    """Retrieve a specific item by ID."""
    items = load_data()
    for item in items:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")



@router.put("/{item_id}", response_model=ItemOut)
def update_item(item_id: str, payload: ItemUpdate):
    """Update an existing item by ID."""
    items = load_data()
    for index, item in enumerate(items):
        updated_item = item.copy()
        if item["id"] == item_id:
            if payload.title is not None:
                updated_item["title"] = payload.title
            if payload.description is not None:
                updated_item["description"] = payload.description
            if payload.priority is not None:
                updated_item["priority"] = payload.priority
            if payload.status is not None:
                updated_item["status"] = payload.status
            items[index] = updated_item
            save_data(items)
            return updated_item
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")





@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: str):
    """Delete an item by ID."""
    items = load_data()
    for index, item in enumerate(items):
        if item["id"] == item_id:
            items.pop(index)
            save_data(items)
            return
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")