from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, code, apps, deploy, session
from app.database import init_db

app = FastAPI(title="AI Web Code Generator API", version="1.0.0")

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()

# 允许所有来源访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(code.router, prefix="/api/code", tags=["code"])
app.include_router(apps.router, prefix="/api/apps", tags=["apps"])
app.include_router(deploy.router, prefix="/api/deploy", tags=["deploy"])
app.include_router(session.router, prefix="/api/session", tags=["session"])

@app.get("/")
async def root():
    return {"message": "AI Web Code Generator API", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
