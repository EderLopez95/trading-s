import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.routes import router
from fastapi.middleware.cors import CORSMiddleware
from app.domain.exceptions import DomainError, ConfigNotFoundError

app = FastAPI()

frontend_url = os.getenv("FRONTEND_URL") or "http://localhost:3000"
origins = [frontend_url]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.exception_handler(ConfigNotFoundError)
async def config_not_found_handler(request: Request, exc: ConfigNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "type": "error",
            "message": str(exc)
        }
    )

@app.exception_handler(DomainError)
async def domain_exception_handler(request: Request, exc: DomainError):
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "type": "error",
            "message": str(exc)
        },
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "type": "error",
            "message": "Internal Server Error: " + str(exc)
        },
    )
