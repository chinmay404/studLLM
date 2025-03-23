from fastapi import APIRouter, HTTPException, Query
from app.models.request import ChatRequest
from app.models.response import ChatResponse
from langcahin_agent.main import getGraphResponse

graph = getGraphResponse()
router = APIRouter()

@router.post("/chat")
async def chat(request: ChatRequest ):
    try:
        query = request.message
        config = {"configurable": {"thread_id":request.user_id}}      
        responset = graph.get_response(query , config ,request.user_id )
        try:
            response_text = responset.content
            message = response_text.split("</think>")[1]
            thinking = response_text.split("</think>")[0]
        except:
            message = responset
            thinking = ""
        return {"message": message , "Thinking" : thinking}


    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
