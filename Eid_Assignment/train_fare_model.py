import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
import pickle

# Load your CSV dataset
df = pd.read_csv("gtfs_training_data.csv")

X = df[["time", "passenger_count", "vehicle_count", "weather", "day_type"]]
y = df["discount"]

# Preprocessing (encode categorical)
X = pd.get_dummies(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = GradientBoostingRegressor()
model.fit(X_train, y_train)

# Save model
with open("fareAI_model.pkl", "wb") as f:
    pickle.dump(model, f)
