from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from models.schemas import GenerateRequest, GenerateResponse, GeneratedCode
from services.ai_service import ai_service

router = APIRouter()

@router.post("/api/generate", response_model=GenerateResponse)
async def generate_code(request: GenerateRequest):
    """生成代码API"""
    try:
        code = await ai_service.generate_code(request.prompt)
        return GenerateResponse(
            message="代码生成成功",
            code=code
        )
    except Exception as e:
        return GenerateResponse(
            message=f"生成失败: {str(e)}",
            code=None
        )

@router.post("/api/stream")
async def stream_generate(request: GenerateRequest):
    """流式生成API"""
    return StreamingResponse(
        ai_service.stream_response(request.prompt),
        media_type="text/event-stream"
    )