from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.api.routes import health, ingest, retrieve


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(title=settings.app_name)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router, prefix=settings.api_prefix, tags=["health"])
    app.include_router(ingest.router, prefix=settings.api_prefix, tags=["ingest"])
    app.include_router(retrieve.router, prefix=settings.api_prefix, tags=["search"])

    @app.get("/")
    def root():
        return {"status": "ok", "app": settings.app_name}

    return app


app = create_app()
