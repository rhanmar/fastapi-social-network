from fastapi import FastAPI

from app.config.database import Base, engine
from app.routers.posts import router as posts_router
from app.routers.users import router as users_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users_router)
app.include_router(posts_router)


@app.get("/")
def read_root():
    return {"FastAPI": "Social Network"}
