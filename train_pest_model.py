import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib

# Dummy dataset (image features simulation)
X = [
    [120, 200, 150],  # pest1
    [30, 50, 80],     # pest2
    [200, 220, 210],  # pest3
]

y = ["Aphids", "Leaf Miner", "Whitefly"]

model = RandomForestClassifier()
model.fit(X, y)

joblib.dump(model, "models/pest_model.pkl")

print("Model trained and saved")