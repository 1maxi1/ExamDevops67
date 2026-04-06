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
from app.models import MetroChange, TravelCard
from app.schemas import BalanceRequest, BalanceResponse, MetroChangeResponse
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
        f"{app_settings.api_prefix}/metro/changes",
        response_model=list[MetroChangeResponse],
        tags=["metro"],
    )
    def get_metro_changes(db: Session = Depends(get_db_session)) -> list[MetroChange]:
        return list(db.scalars(select(MetroChange).order_by(MetroChange.id)).all())

    @app.post(
        f"{app_settings.api_prefix}/travel-card/balance",
        response_model=BalanceResponse,
        tags=["travel-card"],
    )
    def get_travel_card_balance(
        payload: BalanceRequest,
        db: Session = Depends(get_db_session),
    ) -> BalanceResponse:
        travel_card = db.scalar(
            select(TravelCard).where(
                TravelCard.phone == payload.phone,
                TravelCard.sms_code == payload.sms_code,
            )
        )
        if travel_card is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid phone number or SMS code",
            )

        return BalanceResponse(
            ticket_id=travel_card.id,
            phone=travel_card.phone,
            balance=travel_card.balance,
            last_entry_station=travel_card.last_entry_station,
        )

    return app


app = create_app()
