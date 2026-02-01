from app.db.session import engine
from app.models.base import Base
import app.models.document  # noqa: F401 - ensures models are registered


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
