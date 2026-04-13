from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import Settings, get_settings
from app.database import (
    create_engine_from_settings,
    create_session_factory,
    get_db_session,
    init_db,
)
from app.models import WorkshopClass, WorkshopRegistration
from app.schemas import RegistrationRequest, RegistrationResponse, WorkshopClassResponse
from app.seed import seed_initial_data

STATIC_DIR = Path(__file__).parent / "static"


def create_app(settings: Settings | None = None) -> FastAPI:
    app_settings = settings or get_settings()
    engine = create_engine_from_settings(app_settings)
    session_factory = create_session_factory(engine)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        init_db(engine)
        if app_settings.seed_database:
            with session_factory() as session:
                seed_initial_data(session)
        yield
        engine.dispose()

    app = FastAPI(
        title=app_settings.app_title,
        debug=app_settings.debug,
        lifespan=lifespan,
    )
    app.state.engine = engine
    app.state.session_factory = session_factory

    @app.get("/", include_in_schema=False)
    def index() -> FileResponse:
        return FileResponse(STATIC_DIR / "index.html")

    @app.get("/health")
    def healthcheck() -> dict[str, str]:
        return {"status": "ok"}

    @app.get(
        f"{app_settings.api_prefix}/workshops",
        response_model=list[WorkshopClassResponse],
        tags=["workshops"],
    )
    def get_workshop_classes(db: Session = Depends(get_db_session)) -> list[WorkshopClass]:
        return list(db.scalars(select(WorkshopClass).order_by(WorkshopClass.id)).all())

    @app.post(
        f"{app_settings.api_prefix}/registrations/info",
        response_model=RegistrationResponse,
        tags=["registrations"],
    )
    def get_workshop_registration(
        payload: RegistrationRequest,
        db: Session = Depends(get_db_session),
    ) -> RegistrationResponse:
        registration = db.scalar(
            select(WorkshopRegistration).where(
                WorkshopRegistration.sms_code == payload.sms_code,
            )
        )
        if registration is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid SMS code",
            )

        return RegistrationResponse(
            registration_id=registration.id,
            sms_code=registration.sms_code,
            workshop_name=registration.workshop_name,
            registration_time=registration.registration_time,
        )

    return app


app = create_app()
