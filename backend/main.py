
from contextlib import asynccontextmanager

import tensorflow as tf
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

MODEL_PATH = "artifacts/final_ids_model.keras"


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Loading Enhanced IDS model...")
    app.state.model = tf.keras.models.load_model(
        MODEL_PATH,
        compile=False
    )
    print("Enhanced IDS model loaded successfully!")
    yield
    print("Enhanced IDS backend stopped.")


app = FastAPI(
    title="Enhanced IDS API",
    description="API for the Enhanced Intrusion Detection System research prototype.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Enhanced IDS API is running",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    model = getattr(app.state, "model", None)

    return {
        "status": "healthy" if model is not None else "not_ready",
        "model_loaded": model is not None,
    }
