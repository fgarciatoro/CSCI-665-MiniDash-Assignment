from fastapi import FastAPI
from app.database import init_db
from app.routes import router

app = FastAPI(title="MiniDash")
app.include_router(router)

@app.on_event("startup")
def startup() -> None:
    init_db()
