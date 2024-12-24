from main_app.db.db_config.db_config import engine
from ..session.session_maker import session_maker
from ..models.base_model import Base


def init_database():
    with session_maker() as session:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        print("database initialized successfully")

