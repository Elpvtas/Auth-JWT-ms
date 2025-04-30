from fastapi import FastAPI, Depends, HTTPException
from src.app.users.infrastructure.routers.user_router import router as user_router
from src.app.users.infrastructure.routers.user_auth_router import router as auth_router
from src.app.infrastructure.database.db_connection_factory import DatabaseConectionFactory


app = FastAPI(title="Andina Trading Backend")


#@app.on_event("startup")
#def stratup():
    #DatabaseConectionFactory.initialize()

#@app.on_event("shutdown")
#def shutdown():
    #DatabaseConectionFactory.close_pool()

#app.include_router(user_router , prefix="/users" , tags=["Users"])
app.include_router(auth_router)


