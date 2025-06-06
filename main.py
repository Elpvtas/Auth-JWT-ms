from fastapi import FastAPI, Depends, HTTPException
from starlette.middleware.cors import CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware
from src.app.infrastructure.routers.company_router import router as company_router
from src.app.infrastructure.routers.user_router import router as user_router
from src.app.infrastructure.routers.action_router import router as action_router
from src.app.infrastructure.routers.contract_router import router as contract_router
from src.app.infrastructure.routers.order_router import router as order_router

from src.app.infrastructure.database.db_connection_factory import DatabaseConectionFactory


app = FastAPI(title="Andina Trading Backend")

origins = [
    "http://localhost:4200",  # Frontend Angular
    # Agrega más orígenes si es necesario
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permitir solicitudes desde Angular
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def stratup():
    DatabaseConectionFactory.initialize()

@app.on_event("shutdown")
def shutdown():
    DatabaseConectionFactory.close_pool()

app.include_router(user_router , prefix="/users" , tags=["Users"])
app.include_router(company_router, prefix="/companies", tags=["Companies"])
app.include_router(action_router, prefix="/actions", tags=["Actions"])
app.include_router(contract_router, prefix="/contracts", tags=["Contracts"])
app.include_router(order_router, prefix="/order", tags=["Orders"])

