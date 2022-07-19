from fastapi import FastAPI
from core import routes

app = FastAPI(name="Video Upload")

app.include_router(routes.router)


@app.get("/")
def root():
    return "welcome to the api got to /docs for more "
