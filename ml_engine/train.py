import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report
import joblib
from pymongo import MongoClient

def train_and_save_model():
    print("Connecting to MongoDB and loading data...")
    
    client = MongoClient('mongodb://localhost:27017/')
    
    db = client['phishing_Database'] 
    collection = db['dataset']
    
    cursor = collection.find({}, {'_id': 0})
    df = pd.DataFrame(list(cursor))
    
    if df.empty:
        print("Error: No data found in the database. Please check database and collection names.")
        return

    print(f"Data loaded successfully. Total records: {len(df)}")

    X = df.drop('Result', axis=1)
    y = df['Result'].apply(lambda x: 1 if x == 1 else 0)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Training Neural Network...")
    nn_model = MLPClassifier(hidden_layer_sizes=(32, 16), max_iter=500, random_state=42)
    nn_model.fit(X_train, y_train)

    print("Evaluating Model...")
    y_pred = nn_model.predict(X_test)
    print(classification_report(y_test, y_pred))

    print("Saving model artifact...")
    joblib.dump(nn_model, 'phishing_nn_model.pkl')
    print("Model saved successfully as phishing_nn_model.pkl")

if __name__ == "__main__":
    train_and_save_model()