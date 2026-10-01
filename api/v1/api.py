from fastapi import APIRouter
from api.v1.endpoints import user, race, registration, result

api_router = APIRouter()

api_router.include_router(user.router, prefix='/users', tags=['users'])
api_router.include_router(race.router, prefix='/races', tags=['races'])
api_router.include_router(registration.router, prefix='/registrations', tags=['registrations'])
api_router.include_router(result.router, prefix='/results', tags=['results'])
