from fastapi import APIRouter, HTTPException, Query
from app.models.request import ChatRequest
from app.models.response import ChatResponse
from langcahin_agent.main import getGraphResponse

graph = getGraphResponse()
router = APIRouter()

@router.post("/chat")
async def chat(request: ChatRequest):
    try:
        query = request.message
        responset = graph.get_response(query)
        response_text = responset.content
        message = response_text.split("</think>")[1]
        thinking = response_text.split("</think>")[0]
        return {"message": message , "Thinking" : thinking}


    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
