from fastapi import FastAPI, Depends
from pydantic import BaseModel

from modules.LLaMa.LLaMAManager import LLaMAManager
from api.routers.pdf_router import router as pdf_router
from api.routers.skill_matcher_router import router as skill_matcher_router

app = FastAPI()

# Initialize LLaMA manager
llama_manager  = LLaMAManager(
    model_path="neural_networks/llama-pro-8b-instruct.Q4_K_M.gguf",
    n_ctx=4096,
    n_gpu_layers=35
)

def get_llama_manager() -> LLaMAManager:
    """Get the global LLaMA manager instance as a dependency"""
    return llama_manager

# Include routers
app.include_router(pdf_router, prefix="/api", tags=["PDF Operations"])
app.include_router(skill_matcher_router, prefix="/api/skill-matcher", tags=["Skill Matcher"])

# Import and include philosophy router after llama_manager is initialized
from modules.philosophy.philosophy_router import router as philosophy_router
app.include_router(philosophy_router, prefix="/api/philosophy", tags=["Philosophy Analysis"])



class ChatRequest(BaseModel):
    message: str

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/chat")
async def chat_endpoint(request: ChatRequest):

    response = llama_manager.chat(request.message)

    return {"response": response}