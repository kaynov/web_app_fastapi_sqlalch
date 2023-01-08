from datetime import date
from pydantic import BaseModel


class Items_in_store(BaseModel):
    id: int
    name: str


class Stores(BaseModel):
    id: int
    address: str


class SalesIn(BaseModel):
    stores_id: int
    items_id: int


class SalesOut(BaseModel):
    stores_id: int
    items_id: int
    create_date = date


class Top_stores(Stores):
    id: int
    address: str
    tottal_rev: int


class Top_items(BaseModel):
    id: int
    name: str
    goods_sold_count: int


