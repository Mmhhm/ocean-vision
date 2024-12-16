from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from repo import CONN_ROUTE


engine = create_engine(CONN_ROUTE)

session_maker = sessionmaker(bind=engine)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))