from fastapi import FastAPI
from app.core.security import enforce_x_user_id
from app.api.v1.clients import router as clients_router
from app.api.v1.auth import router as auth_router
from app.api.v1.stats import router as stats_router

app = FastAPI()

# Middleware global
app.middleware("http")(enforce_x_user_id)

# Montée des routers
app.include_router(auth_router)
app.include_router(clients_router)
app.include_router(stats_router)
