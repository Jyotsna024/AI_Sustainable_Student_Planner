import numpy as np
import pickle
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedKFold, cross_val_score

BASE_DIR = Path(__file__).resolve().parent
ML_DIR = BASE_DIR / "ml"
MODEL_PATH = ML_DIR / "burnout_model.pkl"

np.random.seed(42)

sleep = np.random.randint(3, 9, 300)
screen = np.random.randint(2, 12, 300)
study = np.random.randint(1, 11, 300)

sleep_debt = np.maximum(0, 8 - sleep)
cognitive_load = 0.6 * study + 0.4 * screen

X = np.column_stack([
    sleep,
    screen,
    study,
    sleep_debt,
    cognitive_load
])

y = np.where(
    (sleep >= 7) & (screen <= 5) & (study <= 5), 0,
    np.where(
        (sleep >= 6) & (screen <= 8) & (study <= 7), 1, 2
    )
)

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(
        solver="lbfgs",
        C=0.8,
        max_iter=3000
    ))
])

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(pipeline, X, y, cv=cv, scoring="accuracy")

pipeline.fit(X, y)

ML_DIR.mkdir(exist_ok=True)
with open(MODEL_PATH, "wb") as f:
    pickle.dump(pipeline, f)

print("Model trained")
print("CV Accuracy:", round(scores.mean(), 3))
print("Model saved at:", MODEL_PATH)
