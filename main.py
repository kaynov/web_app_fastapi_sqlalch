from datetime import date
from typing import List

import databases
from dateutil.relativedelta import relativedelta
from fastapi import FastAPI
from sqlalchemy import create_engine, \
    func, select, desc, literal_column

from models import metadata, stores, sales, items
from schemas import SalesIn, SalesOut, Items_in_store, Top_items, Stores, Top_stores

DATABASE_URL = "postgresql://postgres:s1t@localhost/sqlalchemy_tuts"

database = databases.Database(DATABASE_URL)

engine = create_engine('postgresql://postgres:s1t@localhost/sqlalchemy_tuts')

metadata.create_all(engine)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/items/", response_model=List[Items_in_store])
async def read_items_in_store():
    query = items.select()
    return await database.fetch_all(query)


@app.get("/stores/", response_model=List[Stores])
async def read_stores():
    query = stores.select()
    return await database.fetch_all(query)


@app.post("/sales/", response_model=SalesOut)
async def create_sales(sale: SalesIn):
    query = sales.insert().values(stores_id=sale.stores_id, items_id=sale.items_id, create_date=date.today())
    sale_id = await database.execute(query)
    return sale


@app.get("/stores/total_rev", response_model=List[Top_stores])
async def get_top_sotres():
    sl = sales.alias("sl")
    query = select([stores.c.id.label('id'),
                    stores.c.address.label('address'),
                    func.sum(items.c.price).label('tottal_rev')]
                   ).join(sl, stores.c.id == sl.c.stores_id
                          ).join(items, items.c.id == sl.c.items_id
                                 ).filter(sl.c.create_date >= date.today() + relativedelta(months=-1)
                                          ).group_by(stores.c.id, stores.c.address
                                                     ).order_by(desc(literal_column('tottal_rev'))).limit(
        10)
    return await database.fetch_all(query)


@app.get("/stores/goods_sold_count", response_model=List[Top_items])
async def get_top_items():
    query = select([items.c.id.label('id'),
                    items.c.name.label('name'),
                    func.count(sales.c.id).label('goods_sold_count')
                    ]).select_from(items.join(sales)
                                   ).group_by(items.c.id
                                              ).order_by(desc(literal_column('goods_sold_count'))).limit(
        10)
    return await database.fetch_all(query)


