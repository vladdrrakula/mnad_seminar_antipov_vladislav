import os
import pickle
import pandas as pd
import time
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

def train_model(filename: str, model_name: str, train_size: float):
    path = os.path.join("data", filename)
    df = pd.read_csv(path)

    target = df.columns[-1]
    X = pd.get_dummies(df.drop(columns=[target]), drop_first=True)
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, train_size=train_size, random_state=42
    )

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    time.sleep(5)

    pred = model.predict(X_test)
    acc = accuracy_score(y_test, pred)

    os.makedirs("models", exist_ok=True)
    with open(os.path.join("models", f"{model_name}.pkl"), "wb") as f:
        pickle.dump(model, f)

    return {"accuracy": acc, "model_path": f"models/{model_name}.pkl"}