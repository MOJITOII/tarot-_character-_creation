from typing import TypedDict, Optional, List
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt, Command


class TarotState(TypedDict):
    drawn_cards: List[str]
    card_meanings: List[dict]
    user_background: str
    prompt: Optional[str]
    generated_profile: Optional[str]
    feedback: Optional[str]
    iteration_count: int


def draw_cards(state: TarotState) -> dict:
    from .cards import get_random_cards, get_card_meanings
    keys = get_random_cards()
    meanings = get_card_meanings(keys)
    return {"drawn_cards": keys, "card_meanings": meanings, "iteration_count": 0}


def wait_user_input(state: TarotState) -> dict:
    user_data = interrupt(value="请输入故事背景")
    return {"user_background": user_data["user_background"], "feedback": None}


def build_prompt(state: TarotState) -> dict:
    from .prompts import build_profile_prompt
    prompt = build_profile_prompt(
        state["drawn_cards"],
        state["card_meanings"],
        state["user_background"],
        feedback=state.get("feedback") or ""
    )
    return {"prompt": prompt}


def generate_profile(state: TarotState) -> dict:
    from .llm import generate_profile
    profile = generate_profile(state["prompt"])
    return {"generated_profile": profile}


def wait_feedback(state: TarotState) -> dict:
    user_data = interrupt(value="请输入反馈（可选）")
    feedback = user_data.get("feedback")
    if feedback == "" or feedback is None:
        feedback = None
    return {"feedback": feedback}


def check_satisfaction(state: TarotState) -> Command:
    if state.get("feedback") and state["iteration_count"] < 3:
        return Command(
            goto="build_prompt",
            update={"iteration_count": state["iteration_count"] + 1}
        )
    else:
        return Command(goto=END)


graph = StateGraph(TarotState)
graph.add_node("draw_cards", draw_cards)
graph.add_node("wait_user_input", wait_user_input)
graph.add_node("build_prompt", build_prompt)
graph.add_node("generate_profile", generate_profile)
graph.add_node("wait_feedback", wait_feedback)
graph.add_node("check_satisfaction", check_satisfaction)

graph.set_entry_point("draw_cards")
graph.add_edge("draw_cards", "wait_user_input")
graph.add_edge("wait_user_input", "build_prompt")
graph.add_edge("build_prompt", "generate_profile")
graph.add_edge("generate_profile", "wait_feedback")
graph.add_edge("wait_feedback", "check_satisfaction")

memory = MemorySaver()
app = graph.compile(checkpointer=memory)