"""
description: main file for the project
"Run: uvicorn main:app --reload" --> Optional[host, port, reload]
Author: Prabal Pathak
"""
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from database import database
from authentication.auth_utils import router

database.Base.metadata.create_all(bind=database.engine)  # create all tables
app = FastAPI()

app.include_router(router)


@app.get("/")
async def root() -> JSONResponse:
    """root endpoint
    return : "message"
    """
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000)
