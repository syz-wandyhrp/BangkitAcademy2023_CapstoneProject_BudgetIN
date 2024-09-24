from typing import Union
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter, And

# Initialize Firebase app with credentials
cred = credentials.Certificate('frcredproject.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

app = FastAPI()

class RestoItem(BaseModel):
    max: int
    min: int


@app.get("/")
async def read_root():
    raise HTTPException(status_code=404)


@app.post("/get_resto/")
async def read_item(item:RestoItem):
    item_dict = item.dict()
    print(item.min, item.max)
    docs = db.collection(u'restaurant_V3')
    docs = docs.where(filter=FieldFilter('max_price','<=',item.max))
    # docs.where(filter=FieldFilter('min_price','>=',item.min))
    dstream = docs.stream()
    ts=[]
    for doc in dstream:
        # print(f'{doc.id} => {doc.to_dict()}')
        dc = doc.to_dict()
        mp = dc['min_price']
        maxp = dc['max_price']
        print(mp,maxp)
        if mp >= item.min:
            dc['min_price'] = maxp
            dc['max_price'] = mp
            ts.append(dc)
    return {"status": 'ok',"data": ts}
