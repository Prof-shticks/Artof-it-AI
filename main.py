from fastapi import FastAPI
from pydantic import BaseModel

from modules.LLaMa.LLaMAManager import LLaMAManager
from api.routers.pdf_router import router as pdf_router

app = FastAPI()

# Include routers
app.include_router(pdf_router, prefix="/api", tags=["PDF Operations"])

llama_manager  = LLaMAManager(
    model_path="neural_networks/llama-pro-8b-instruct.Q4_K_M.gguf",
    n_ctx=4096,
    n_gpu_layers=35
)
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