from sqlalchemy import MetaData, Table, String, Integer, Column, ForeignKey, Date
from datetime import date

from sqlalchemy import MetaData, Table, String, Integer, Column, ForeignKey, Date

metadata = MetaData()

sales = Table(
    "sales",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("stores_id", ForeignKey("stores.id")),
    Column("items_id", ForeignKey("items.id")),
    Column("create_date", Date, default=date.today())
)

items = Table(
    "items",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, index=True),
    Column("price", Integer)
)

stores = Table(
    "stores",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("address", String, index=True)
)

