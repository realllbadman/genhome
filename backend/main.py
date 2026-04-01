from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from backend.database import engine, Base
from backend.routes import bookings, admin, orders

app = FastAPI(title="Generator Business API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(bookings.router, prefix="/api/bookings", tags=["bookings"])
app.include_router(orders.router, prefix="/api/orders", tags=["orders"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])

frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.isdir(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def serve_index():
    index_path = os.path.join(frontend_path, "index.html")
    return FileResponse(index_path)


@app.get("/admin")
def serve_admin():
    admin_path = os.path.join(frontend_path, "admin.html")
    return FileResponse(admin_path)


@app.get("/about")
def serve_about():
    about_path = os.path.join(frontend_path, "about.html")
    return FileResponse(about_path)
