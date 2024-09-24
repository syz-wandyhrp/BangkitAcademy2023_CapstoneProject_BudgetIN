import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd

# Initialize Firebase app with credentials
cred = credentials.Certificate('frcredproject.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

df = pd.read_csv('dataset_rest_V1.csv')
grouped = df.groupby(['merchant_name','merchant_area','coordinate'])
aggregated = grouped['price'].agg(['min', 'max']).reset_index()

for d in aggregated.index:
    dmn = aggregated['merchant_name'][d]
    dmr = aggregated['merchant_area'][d]
    dmin = aggregated['min'][d]
    dmax = aggregated['max'][d]
    coordinate = aggregated['coordinate'][d]
    coordinate = coordinate.split(",")
    dlat = coordinate[0]  # Replace 'latitude' with the actual column name
    dlon = coordinate[1]  # Replace 'longitude' with the actual column name
    
    print(f"Inserting {dmn}....")    
    data = {
        u'name': dmn,
        u'min_price': dmin,
        u'max_price': dmax,
        u'merchant_area': dmr,
    }
    if not pd.isnull(dlat) and not pd.isnull(dlon):
        # Convert latitude and longitude to Firestore GeoPoint
        data[u'location'] = firestore.GeoPoint(float(dlat), float(dlon))
    try:
        db.collection(u'restaurant_V3').add(data)
    except Exception as e:
        print(f"Error inserting {dmn}: {e}")
