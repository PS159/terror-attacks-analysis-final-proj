from sqlalchemy.orm import sessionmaker, scoped_session

from main_app.db.db_config.db_config import engine


session_maker = sessionmaker(bind=engine)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))