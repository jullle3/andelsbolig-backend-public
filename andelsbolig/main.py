import os
import sys
from os.path import abspath, dirname

# Add whole project to sys.path
current_dir = dirname(abspath(__file__))
parent_dir = dirname(current_dir)
sys.path.append(parent_dir)

import uvicorn
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse, Response
from fastapi.middleware.cors import CORSMiddleware

from andelsbolig.config.properties import DISABLE_ACCESS_LOGS, WORKERS
import andelsbolig.advertisement.controller
import andelsbolig.agent.controller
import andelsbolig.upload.controller
import andelsbolig.user.controller
import andelsbolig.payment.controller
import andelsbolig.comment_thread.controller
import andelsbolig.cron_tasks
from andelsbolig.misc.logger import get_logger
from andelsbolig.security.service import decode_jwt, extract_jwt, is_subscribed, is_authenticated
import logging

logging.getLogger("uvicorn.access").disabled = DISABLE_ACCESS_LOGS

app = FastAPI()
logger = get_logger(__name__)
# check_for_upgrade()

# # Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
def read_root():
    return {"message": "Welcome to andelsboligbasen 🚀"}


@app.get("/is-authenticated")
def is_authenticated(_=Depends(is_authenticated)):
    """Hvis dette endpoint kan nås er du authenticated/logget ind"""
    return "True"


@app.get("/is-subscribed")
def is_subscribed_endpoint(_=Depends(is_subscribed)):
    """Hvis dette endpoint kan nås er du authenticated/logget ind og har et aktivt abonnement"""
    return "True"


# TODO: Why is this needed?
@app.options("/{rest_of_path:path}")
async def preflight_handler(request: Request, rest_of_path: str):
    """Preflight handler for all endpoints which is needed for CORS"""
    return Response(status_code=200)


app.include_router(andelsbolig.advertisement.controller.router)
app.include_router(andelsbolig.agent.controller.router)
app.include_router(andelsbolig.user.controller.router)
app.include_router(andelsbolig.upload.controller.router)
app.include_router(andelsbolig.payment.controller.router)
app.include_router(andelsbolig.comment_thread.controller.router)
app.include_router(andelsbolig.cron_tasks.router)

whitelisted_get_endpoints = ["/", "/advertisement", "/docs", "/openapi.json"]
whitelisted_post_endpoints = ["/user", "/login", "/webhook"]


# @app.middleware("http")
# async def authenticate(request: Request, call_next):
#     # Some endpoints are whitelisted
#     # skip_msg = f"{request.method} {request.url.path} skipped authentication"
#     if request.method == "GET" and request.url.path in whitelisted_get_endpoints:
#         pass
#         # logger.info(skip_msg)
#     elif request.method == "POST" and request.url.path in whitelisted_post_endpoints:
#         pass
#         # logger.info(skip_msg)
#     elif request.method == "OPTIONS":
#         pass
#         # logger.info(skip_msg)
#     else:
#         try:
#             jwt = extract_jwt(request)
#             decode_jwt(jwt, verify=True)
#         except HTTPException as e:
#             headers = {"Access-Control-Allow-Origin": "*"}  # Adjust the headers as necessary
#             logger.info(f"Denied request to {request.url.path} {e.status_code=} {e.detail=}")
#             return JSONResponse(status_code=e.status_code, content={"detail": e.detail}, headers=headers)
#             # TODO: fix redirects
#             # return RedirectResponse(url=f'{FRONTEND_URL}/index.html?view=login', headers=headers, status_code=303)
#     response = await call_next(request)
#     return response


if __name__ == "__main__":
    uvicorn.run("andelsbolig.main:app", port=int(os.environ.get("PORT", 8500)), workers=2, host="0.0.0.0")
    # uvicorn.run("andelsbolig.main:app", port=int(os.environ.get("PORT", 8500)), workers=WORKERS, host="0.0.0.0")
