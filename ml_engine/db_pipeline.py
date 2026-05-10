import pandas as pd
from pymongo import MongoClient

def setup_database():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['phishing_Database']
    collection = db['dataset']

    print("Reading dataset...")
    df = pd.read_csv('../data/phishingData.csv')
    records = df.to_dict(orient='records')

    collection.delete_many({})
    collection.insert_many(records)
    print(f"Inserted {collection.count_documents({})} records.")

    pipeline1 = [
        {"$group": {"_id": "$SSLfinal_State", "value": {"$sum": 1}}},
        {"$out": "ssl_state_counts"}  
    ]
    collection.aggregate(pipeline1)
    print("Aggregation Job 1 complete: ssl_state_counts created.")

    pipeline2 = [
        {"$group": {"_id": "$Result", "value": {"$sum": "$web_traffic"}}},
        {"$out": "traffic_phishing_distribution"} 
    ]
    collection.aggregate(pipeline2)
    print("Aggregation Job 2 complete: traffic_phishing_distribution created.")

if __name__ == "__main__":
    setup_database()