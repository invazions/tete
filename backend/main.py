from fastapi import FastAPI

from hosts import router as hosts_router
from users import router as users_router

app = FastAPI(
    title="Sanoptes",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)

app.include_router(hosts_router)
app.include_router(users_router)
