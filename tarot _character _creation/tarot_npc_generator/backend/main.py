import os
import uuid
import urllib.parse
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from langgraph.types import Command
from .graph import app as graph_app


app = FastAPI(title="塔罗牌NPC生成器")

base_dir = os.path.dirname(os.path.dirname(__file__))
app.mount("/data", StaticFiles(directory=os.path.join(base_dir, "data")), name="data")
app.mount("/static", StaticFiles(directory=os.path.join(base_dir, "frontend")), name="static")


class ContinueRequest(BaseModel):
    thread_id: str = Field(..., description="会话ID")
    user_background: str = Field(default="", description="故事背景")
    feedback: str = Field(default="", description="反馈内容")


def get_card_image_url(card_key: str) -> str:
    card_num = card_key.split("_")[0]
    card_name = card_key.split("_")[1]
    encoded_name = urllib.parse.quote(f"{card_num}_{card_name}.png")
    return f"/data/image/{encoded_name}"


@app.get("/")
async def root():
    return FileResponse(os.path.join(base_dir, "frontend", "index.html"))


@app.post("/start")
def start_session():
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    try:
        result = graph_app.invoke({}, config)
    except Exception as e:
        result = None
    
    if result is None or "__interrupt__" in (result if isinstance(result, dict) else {}):
        state = graph_app.get_state(config)
        if state:
            drawn_cards = state.values.get("drawn_cards", [])
            card_images = [get_card_image_url(card) for card in drawn_cards]
            return {
                "thread_id": thread_id,
                "drawn_cards": drawn_cards,
                "card_images": card_images,
                "status": "waiting_background"
            }
        raise HTTPException(status_code=500, detail="会话创建失败")
    
    drawn_cards = result.get("drawn_cards", [])
    card_images = [get_card_image_url(card) for card in drawn_cards]
    return {
        "thread_id": thread_id,
        "drawn_cards": drawn_cards,
        "card_images": card_images,
        "status": "waiting_background"
    }


@app.post("/continue")
def continue_session(req: ContinueRequest):
    thread_id = req.thread_id
    config = {"configurable": {"thread_id": thread_id}}
    
    state = graph_app.get_state(config)
    if not state:
        raise HTTPException(status_code=404, detail="会话不存在")
    
    current_values = state.values
    is_first_continue = current_values.get("user_background") is None
    
    resume_data = {}
    if is_first_continue:
        resume_data["user_background"] = req.user_background
    else:
        resume_data["feedback"] = req.feedback
    
    try:
        result = graph_app.invoke(Command(resume=resume_data), config)
    except Exception as e:
        result = None
    
    if result is None or "__interrupt__" in (result if isinstance(result, dict) else {}):
        new_state = graph_app.get_state(config)
        new_values = new_state.values if new_state else {}
        
        generated_profile = new_values.get("generated_profile")
        feedback_state = new_values.get("feedback")
        
        if generated_profile:
            return {
                "thread_id": thread_id,
                "generated_profile": generated_profile,
                "status": "waiting_feedback" if feedback_state is None else "completed"
            }
        raise HTTPException(status_code=500, detail="继续会话失败")
    
    generated_profile = result.get("generated_profile")
    return {
        "thread_id": thread_id,
        "generated_profile": generated_profile,
        "status": "completed"
    }