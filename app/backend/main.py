from fastapi import FastAPI
from routers.ai_router import ai_router

app = FastAPI(title="AI代码生成API", version="1.0.0")


# 注册路由
app.include_router(ai_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)