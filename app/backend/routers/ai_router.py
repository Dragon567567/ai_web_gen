import logging

from fastapi import APIRouter

from services.ai_service import ai_service
from vo.common import UserAppReqVO, success_result

# Set up logging
logger = logging.getLogger(__name__)

ai_router = APIRouter(prefix="/api/v1/ai", tags=["AI"])

@ai_router.post("/gen_code")
def gen_code(req_vo: UserAppReqVO):
    return success_result(ai_service.gen_code(req_vo.desc))