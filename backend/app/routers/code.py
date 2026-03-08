from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
import json
import time

from app.database import get_db
from app.models import models
from app.schemas import schemas
from app.routers.auth import get_current_user
from app.utils.ai_generator import generate_code, modify_code

router = APIRouter()


def generate_progress_events(prompt: str, db: Session, current_user):
    """生成进度事件的 generator"""

    # 步骤1: 解析需求
    yield json.dumps({"step": "parsing", "message": "正在解析需求...", "progress": 10}, ensure_ascii=False) + "\n"
    time.sleep(0.5)

    # 步骤2: AI 生成代码
    yield json.dumps({"step": "generating", "message": "AI 正在生成代码...", "progress": 30}, ensure_ascii=False) + "\n"

    try:
        generated_code = generate_code(prompt)

        # 步骤3: AI 审查代码
        yield json.dumps({"step": "reviewing", "message": "AI 正在审查代码...", "progress": 60}, ensure_ascii=False) + "\n"
        time.sleep(0.5)

        # 步骤4: 整理代码
        yield json.dumps({"step": "organizing", "message": "正在整理代码...", "progress": 80}, ensure_ascii=False) + "\n"

        # 解析文件列表
        try:
            files = json.loads(generated_code)
        except:
            files = []

        # 保存到历史记录
        code_history = models.CodeHistory(
            prompt=prompt,
            generated_code=generated_code,
            user_id=current_user.id
        )
        db.add(code_history)
        db.commit()
        db.refresh(code_history)

        # 步骤5: 完成
        yield json.dumps({
            "step": "completed",
            "message": "代码生成完成！",
            "progress": 100,
            "files": [schemas.CodeFile(filename=f.get('filename', ''), content=f.get('content', ''), folder=f.get('folder', 'frontend')).model_dump() for f in files]
        }, ensure_ascii=False) + "\n"

    except Exception as e:
        yield json.dumps({"step": "error", "message": f"生成失败: {str(e)}", "progress": 0}, ensure_ascii=False) + "\n"


@router.post("/generate/stream")
def create_code_stream(
    request: schemas.CodeGenerateRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """流式返回代码生成进度"""

    return StreamingResponse(
        generate_progress_events(request.prompt, db, current_user),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


@router.post("/generate", response_model=List[schemas.CodeFile])
def create_code(
    request: schemas.CodeGenerateRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # 调用 AI 生成代码
    generated_code = generate_code(request.prompt)

    # 解析文件列表
    try:
        files = json.loads(generated_code)
    except:
        files = []

    # 保存到历史记录
    code_history = models.CodeHistory(
        prompt=request.prompt,
        generated_code=generated_code,
        user_id=current_user.id
    )
    db.add(code_history)
    db.commit()
    db.refresh(code_history)

    # 返回文件列表
    return [schemas.CodeFile(filename=f.get('filename', ''), content=f.get('content', ''), folder=f.get('folder', 'frontend')) for f in files]


@router.post("/modify", response_model=List[schemas.CodeFile])
def modify_code_by_feedback(
    request: schemas.CodeModifyRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """根据用户反馈修改代码"""
    # 调用 AI 修改代码
    modified_code = modify_code(request.original_code, request.feedback)

    # 解析文件列表
    try:
        files = json.loads(modified_code)
    except:
        files = []

    # 返回修改后的文件列表
    return [schemas.CodeFile(filename=f.get('filename', ''), content=f.get('content', ''), folder=f.get('folder', 'frontend')) for f in files]


@router.get("/history", response_model=List[schemas.CodeGenerateResponse])
def get_history(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    history = db.query(models.CodeHistory).filter(
        models.CodeHistory.user_id == current_user.id
    ).order_by(models.CodeHistory.created_at.desc()).all()
    return history

@router.get("/history/{history_id}", response_model=schemas.CodeGenerateResponse)
def get_history_detail(
    history_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    history = db.query(models.CodeHistory).filter(
        models.CodeHistory.id == history_id,
        models.CodeHistory.user_id == current_user.id
    ).first()

    if not history:
        raise HTTPException(status_code=404, detail="History not found")

    return history
