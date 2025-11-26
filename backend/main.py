from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.db import init_db
from routers.scan import router as scan_router
from routers.vpn import router as vpn_router

app = FastAPI(title="WiFi Guardian", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()

app.include_router(scan_router)
app.include_router(vpn_router)

@app.get("/")
def home():
    return {"status": "WiFi Guardian Backend LIVE 🔥", "docs": "/docs"}
