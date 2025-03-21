# from fastapi import FastAPI

# from langcahin_agent.main import getGraphResponse
# from pydantic import BaseModel
# from typing import Dict, Any

# load_dotenv()
# myclient = pymongo.MongoClient("mongodb://localhost:27017/")

# app = FastAPI()
# db = MongoCRUD()


# origins = [
#     "*"
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# graph = getGraphResponse()
# @app.get("/")
# def read_root():
#     return {"message": "Welcome to FastAPI with CORS enabled!"}


# class ChatRequest(BaseModel):
#     message: str

# @app.post("/chat")
# async def chat(request: ChatRequest):
#     query = request.message
#     responset = graph.get_response(query)
#     response_text = responset.content
#     message = response_text.split("</think>")[1]
#     thinking = response_text.split("</think>")[0]
#     return {"message": message , "Thinking" : thinking}


from fastapi import FastAPI
from app.routers import ai_response
import uvicorn
from contextlib import asynccontextmanager
from langcahin_agent.main import getGraphResponse
from fastapi.middleware.cors import CORSMiddleware
# from dotenv import load_dotenv
import pymongo
from DB_ops.main import MongoCRUD


@asynccontextmanager
async def _init_graph(app: FastAPI):
    print("")
    graph = getGraphResponse()
    if not graph:
        raise RuntimeError(
            "Failed To Init LLM Graph")
    else:
        print("Finished checking LLM.")
    yield


app = FastAPI(
    title="studLLm API",
    description="A studLLm API",
    version="1.0.0",
    lifespan=_init_graph
)


origins = [
    "*"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ai_response.router, prefix="/api/v1", tags=["Chat"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
