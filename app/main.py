from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import Api
from .db.database import Base, DB_engine

app = FastAPI(title="satchi-pay")

app.include_router(Api)

@app.get('/')
def welcomeMessage():
    return {
        "message":"welcome to satchi-pay" 
    }


allowed_origins = [
    "http://localhost:8000",
    "http://localhost:5173",
    "http://localhost:5174",
    "https://satchipay.netlify.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins= allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
