from fastapi import APIRouter

from apis.version1 import route_user,route_jobs,route_login

api_router = APIRouter()

api_router.include_router(route_user.router,prefix="/users",tags=["users"])
api_router.include_router(route_jobs.router,prefix="/jobs",tags=["jobs"])
api_router.include_router(route_login.router,prefix="/login",tags=["login"])
