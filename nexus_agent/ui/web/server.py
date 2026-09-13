"""
FastAPI Server for Nexus-Agent Web Mission Control.
Provides RESTful APIs and WebSocket live event streaming for the Glassmorphism Dashboard.
"""

import asyncio
import json
from pathlib import Path
from typing import Dict, List, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel

from nexus_agent.version import __version__
from nexus_agent.core.schema import AgentConfig, AgentStatus
from nexus_agent.core.agent import NexusAgent
from nexus_agent.tools import create_default_registry

app = FastAPI(title="Nexus-Agent Mission Control", version=__version__)

STATIC_DIR = Path(__file__).parent / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Active WebSocket connections
active_connections: List[WebSocket] = []
latest_agent_state: Dict = {}


class RunRequest(BaseModel):
    goal: str
    provider: str = "mock"
    model: str = "mock-model"
    max_iterations: int = 25
    api_key: Optional[str] = None


async def broadcast_event(event_type: str, data: dict):
    message = json.dumps({"type": event_type, "data": data})
    disconnected = []
    for connection in active_connections:
        try:
            await connection.send_text(message)
        except Exception:
            disconnected.append(connection)
    for d in disconnected:
        if d in active_connections:
            active_connections.remove(d)


@app.api_route("/", methods=["GET", "HEAD"], response_class=HTMLResponse)
async def serve_index():
    index_path = STATIC_DIR / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return "<h1>Nexus-Agent Mission Control</h1><p>Static index.html not yet initialized.</p>"


@app.get("/api/status")
async def get_status():
    return {
        "status": "online",
        "version": __version__,
        "active_clients": len(active_connections),
        "latest_state": latest_agent_state
    }


@app.get("/api/tools")
async def get_tools():
    registry = create_default_registry()
    return [
        {
            "name": t.name,
            "category": t.category.value,
            "description": t.description
        }
        for t in registry.list_tools()
    ]


@app.get("/api/snapshots")
async def get_snapshots():
    from nexus_agent.core.memory import PersistentKnowledgeStore
    store = PersistentKnowledgeStore()
    return store.list_snapshots(limit=10)


class RollbackRequest(BaseModel):
    snapshot_id: int


@app.post("/api/rollback")
async def rollback_endpoint(req: RollbackRequest):
    from nexus_agent.core.memory import PersistentKnowledgeStore
    store = PersistentKnowledgeStore()
    try:
        result = store.rollback_snapshot(req.snapshot_id)
        await broadcast_event("time_travel_rollback", result)
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}


def run_agent_task(req: RunRequest, loop: asyncio.AbstractEventLoop):
    config = AgentConfig(
        provider=req.provider,
        model=req.model,
        max_iterations=req.max_iterations,
        api_key=req.api_key
    )
    agent = NexusAgent(config=config)

    def event_callback(event_type: str, data: dict):
        asyncio.run_coroutine_threadsafe(broadcast_event(event_type, data), loop)

    agent.register_callback(event_callback)
    final_state = agent.run(req.goal)
    global latest_agent_state
    latest_agent_state = final_state.model_dump()
    asyncio.run_coroutine_threadsafe(
        broadcast_event("run_finished", latest_agent_state), loop
    )


# Interactive Chat Sessions
chat_sessions: Dict[str, NexusAgent] = {}


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"
    provider: str = "mock"
    model: str = "mock-model"
    api_key: Optional[str] = None


@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    """Multi-turn conversational endpoint with persistent session memory."""
    session_id = req.session_id or "default"
    if session_id not in chat_sessions:
        config = AgentConfig(
            provider=req.provider,
            model=req.model,
            max_iterations=10,
            api_key=req.api_key
        )
        agent = NexusAgent(config=config)
        chat_sessions[session_id] = agent
    else:
        agent = chat_sessions[session_id]

    loop = asyncio.get_event_loop()

    def chat_event_callback(event_type: str, data: dict):
        asyncio.run_coroutine_threadsafe(broadcast_event(event_type, data), loop)

    agent.register_callback(chat_event_callback)

    # Broadcast user message
    await broadcast_event("chat_message", {
        "sender": "user",
        "message": req.message,
        "session_id": session_id
    })

    # Run agent step
    state = agent.run(req.message)
    reply = state.final_output or "응답을 생성하였습니다."

    # Broadcast agent reply
    await broadcast_event("chat_message", {
        "sender": "agent",
        "message": reply,
        "session_id": session_id
    })

    return {
        "status": "success",
        "session_id": session_id,
        "reply": reply
    }


@app.post("/api/run")
async def start_run(req: RunRequest, background_tasks: BackgroundTasks):
    loop = asyncio.get_event_loop()
    background_tasks.add_task(run_agent_task, req, loop)
    return {"status": "started", "goal": req.goal}


@app.websocket("/ws/stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        # Send initial status
        await websocket.send_text(json.dumps({
            "type": "welcome",
            "data": {
                "message": "Connected to Nexus-Agent Real-Time Stream",
                "version": __version__
            }
        }))
        while True:
            # Keep-alive ping/pong
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        if websocket in active_connections:
            active_connections.remove(websocket)
