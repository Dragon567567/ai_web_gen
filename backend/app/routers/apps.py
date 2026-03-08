from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import models
from app.schemas import schemas
from app.routers.auth import get_current_user

router = APIRouter()

@router.get("", response_model=schemas.AppListResponse)
def get_apps(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    query = db.query(models.App).filter(models.App.user_id == current_user.id)
    total = query.count()
    apps = query.order_by(models.App.created_at.desc()).offset(skip).limit(limit).all()

    return {"apps": apps, "total": total}

@router.post("", response_model=schemas.AppResponse)
def create_app(
    app: schemas.AppCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_app = models.App(
        name=app.name,
        description=app.description,
        code=app.code,
        user_id=current_user.id,
        is_published=1
    )
    db.add(db_app)
    db.commit()
    db.refresh(db_app)

    return db_app

@router.get("/{app_id}", response_model=schemas.AppResponse)
def get_app(
    app_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    app = db.query(models.App).filter(
        models.App.id == app_id,
        models.App.user_id == current_user.id
    ).first()

    if not app:
        raise HTTPException(status_code=404, detail="App not found")

    return app

@router.put("/{app_id}", response_model=schemas.AppResponse)
def update_app(
    app_id: int,
    app_update: schemas.AppUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    app = db.query(models.App).filter(
        models.App.id == app_id,
        models.App.user_id == current_user.id
    ).first()

    if not app:
        raise HTTPException(status_code=404, detail="App not found")

    if app_update.name is not None:
        app.name = app_update.name
    if app_update.description is not None:
        app.description = app_update.description
    if app_update.code is not None:
        app.code = app_update.code
    if app_update.is_published is not None:
        app.is_published = app_update.is_published

    db.commit()
    db.refresh(app)

    return app

@router.delete("/{app_id}")
def delete_app(
    app_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    app = db.query(models.App).filter(
        models.App.id == app_id,
        models.App.user_id == current_user.id
    ).first()

    if not app:
        raise HTTPException(status_code=404, detail="App not found")

    db.delete(app)
    db.commit()

    return {"message": "App deleted successfully"}
