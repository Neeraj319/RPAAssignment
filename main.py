from fastapi import FastAPI
from core import routes


app = FastAPI(title="Video Upload")


app.include_router(routes.router)


@app.get("/")
def root():
    return "welcome to the api go to /docs for more "
