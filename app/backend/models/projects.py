from core.database import Base
from sqlalchemy import Column, DateTime, Integer, String


class Projects(Base):
    __tablename__ = "projects"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    user_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    prompt = Column(String, nullable=False)
    html_code = Column(String, nullable=True)
    css_code = Column(String, nullable=True)
    js_code = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), nullable=True)