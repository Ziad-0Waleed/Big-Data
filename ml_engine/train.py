import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report
import joblib

def train_and_save_model():
    print("Loading data for training...")
    df = pd.read_csv('../data/phishingData.csv')
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