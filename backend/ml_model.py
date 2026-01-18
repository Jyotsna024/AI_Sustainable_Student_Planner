import pickle
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "ml" / "burnout_model.pkl"

model = pickle.load(open(MODEL_PATH,"rb"))

def predict_burnout_with_confidence(sleep,screen,study):
    sleep_debt=max(0,8-sleep)
    cognitive_load=0.6*study+0.4*screen
    X=np.array([[sleep,screen,study,sleep_debt,cognitive_load]])
    probs=model.predict_proba(X)[0]
    pred=int(np.argmax(probs))
    confidence=float(np.max(probs))
    features=["sleep","screen","study","sleep_debt","cognitive_load"]
    values=X[0]
    drivers=[f for f,_ in sorted(zip(features,values),key=lambda x:abs(x[1]),reverse=True)[:2]]
    return pred,confidence,drivers
