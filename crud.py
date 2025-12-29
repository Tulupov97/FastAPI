from fastapi import FastAPI, Depends, Query, HTTPException
from pydantic import BaseModel
from starlette import status
from starlette.requests import Request

log_user = []


def log_client(request: Request):
    log_user.append(request.headers)


app = FastAPI(dependencies=[Depends(log_client)])

async def pagination_path_func(page: int):
    if page < 0:
        raise HTTPException(status_code=404, detail="Page does not exist")
    if page == 0:
        raise HTTPException(status_code=400, detail="Invalid page value")

@app.get("/log_user")
async def print_log_user():
    return {"user": log_user}

async def pagination_func(limit: int = Query(10, ge=0), page: int = 1):
    return {'limit': limit, 'page': page}


@app.get("/messages", dependencies=[Depends(pagination_path_func)])
async def all_messages(pagination: dict = Depends(pagination_func)):
    return {"messages": pagination}