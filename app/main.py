from fastapi import FastAPI
from app.database import Base, engine
from app.models import notes as notes_models   # ensures Note is registered for create_all
from app.routers import notes as notes_router

app = FastAPI(title="Notes API")

Base.metadata.create_all(bind=engine)

app.include_router(notes_router.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)