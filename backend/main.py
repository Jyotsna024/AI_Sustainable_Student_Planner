from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.models import StudentInput
from backend.ai_engine import generate_plan

app = FastAPI()

# 🔥 CORS MUST BE HERE, BEFORE ROUTES
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "API is running"}

@app.post("/generate")
def generate(data: StudentInput):
    result = generate_plan(data)
    return result
