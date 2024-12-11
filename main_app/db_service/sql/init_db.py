from main_app.db_config.postgres_conn import create_engine
from base_model import Base


# Initialize the engine and create all the tables
def init_db():
    engine = create_engine("postgresql://username:password@localhost/dbname")
    Base.metadata.create_all(engine)