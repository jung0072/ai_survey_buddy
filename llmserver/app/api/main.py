from fastapi import APIRouter

from app.api.routes import conversation, inference, compile, local_llm

api_router = APIRouter()
api_router.include_router(
    conversation.router, prefix="/conversation", tags=["conversation"]
)
api_router.include_router(inference.router, prefix="/inference", tags=["inference"])
api_router.include_router(compile.router, prefix="/compile", tags=["compile"])
api_router.include_router(local_llm.router, prefix="/local_llm", tags=["local_llm"])
