from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json

from app.database import get_db
from app.models import models
from app.schemas import schemas
from app.routers.auth import get_current_user

router = APIRouter()


@router.post("/sessions", response_model=schemas.ChatSessionResponse)
def create_session(
    request: schemas.CreateSessionRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """创建新会话"""
    session = models.ChatSession(
        title=request.title or "新会话",
        user_id=current_user.id
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    return session


@router.get("/sessions", response_model=List[schemas.ChatSessionResponse])
def get_sessions(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """获取用户的所有会话"""
    sessions = db.query(models.ChatSession).filter(
        models.ChatSession.user_id == current_user.id
    ).order_by(models.ChatSession.updated_at.desc()).all()
    return sessions


@router.get("/sessions/{session_id}", response_model=schemas.ChatSessionDetailResponse)
def get_session_detail(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """获取会话详情（包括消息列表）"""
    session = db.query(models.ChatSession).filter(
        models.ChatSession.id == session_id,
        models.ChatSession.user_id == current_user.id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")

    # 获取消息列表
    messages = db.query(models.ChatMessage).filter(
        models.ChatMessage.session_id == session_id
    ).order_by(models.ChatMessage.created_at.asc()).all()

    # 转换消息格式
    message_list = []
    for msg in messages:
        files = []
        if msg.files:
            try:
                files = json.loads(msg.files)
            except:
                pass

        message_list.append({
            "id": msg.id,
            "role": msg.role,
            "content": msg.content,
            "files": files,
            "created_at": msg.created_at
        })

    return {
        "id": session.id,
        "title": session.title,
        "messages": message_list,
        "created_at": session.created_at,
        "updated_at": session.updated_at
    }


@router.put("/sessions/{session_id}", response_model=schemas.ChatSessionResponse)
def update_session(
    session_id: int,
    request: schemas.UpdateSessionRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """更新会话标题"""
    session = db.query(models.ChatSession).filter(
        models.ChatSession.id == session_id,
        models.ChatSession.user_id == current_user.id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")

    if request.title:
        session.title = request.title

    db.commit()
    db.refresh(session)

    return session


@router.post("/sessions/{session_id}/messages", response_model=schemas.ChatMessageResponse)
def add_message(
    session_id: int,
    request: schemas.AddMessageRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """添加消息到会话"""
    session = db.query(models.ChatSession).filter(
        models.ChatSession.id == session_id,
        models.ChatSession.user_id == current_user.id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")

    # 保存消息
    message = models.ChatMessage(
        session_id=session_id,
        role=request.role,
        content=request.content,
        files=json.dumps([f.model_dump() for f in request.files], ensure_ascii=False) if request.files else None
    )
    db.add(message)

    # 更新会话时间
    from sqlalchemy.sql import func
    session.updated_at = func.now()

    # 如果是用户消息，更新会话标题
    if request.role == "user" and session.title == "新会话":
        # 使用消息内容作为标题（截取前50个字符）
        session.title = request.content[:50] + ("..." if len(request.content) > 50 else "")

    db.commit()
    db.refresh(message)

    # 返回消息
    return {
        "id": message.id,
        "role": message.role,
        "content": message.content,
        "files": [f.model_dump() for f in request.files],
        "created_at": message.created_at
    }


@router.delete("/sessions/{session_id}")
def delete_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """删除会话"""
    session = db.query(models.ChatSession).filter(
        models.ChatSession.id == session_id,
        models.ChatSession.user_id == current_user.id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")

    db.delete(session)
    db.commit()

    return {"message": "删除成功"}