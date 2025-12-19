import os
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier

DATASET_PATH = "dataset"

X = []
y = []

for label in os.listdir(DATASET_PATH):
    label_folder = os.path.join(DATASET_PATH, label)

    if not os.path.isdir(label_folder):
        continue

    for file in os.listdir(label_folder):
        file_path = os.path.join(label_folder, file)
        data = np.loadtxt(file_path)
        X.append(data)
        y.append(label)

X = np.array(X)
y = np.array(y)

print("Training model...")
model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained and saved as model.pkl")
