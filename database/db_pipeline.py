import pandas as pd
from pymongo import MongoClient
from bson.code import Code


def setup_database():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['network_security']
    collection = db['phishing_data']

    print("Reading dataset...")
    df = pd.read_csv('../data/phishingData.csv')
    records = df.to_dict(orient='records')


    collection.delete_many({})
    collection.insert_many(records)
    print(f"Inserted {collection.count_documents({})} records.")

    map1 = Code("function() { emit(this.SSLfinal_State, 1); }")
    reduce1 = Code("function(key, values) { return Array.sum(values); }")
    collection.map_reduce(map1, reduce1, "ssl_state_counts")
    print("MapReduce Job 1 complete: ssl_state_counts created.")

    map2 = Code("function() { emit(this.Result, this.web_traffic); }")
    reduce2 = Code("function(key, values) { return Array.sum(values); }")
    collection.map_reduce(map2, reduce2, "traffic_phishing_distribution")
    print("MapReduce Job 2 complete: traffic_phishing_distribution created.")


if __name__ == "__main__":
    setup_database()