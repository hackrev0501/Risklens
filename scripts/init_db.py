from backend.app.database import engine
from backend.app.models.base import Base
from backend.app.models import user, asset, scan, vuln, ticket, alert  # noqa

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("DB initialized")
