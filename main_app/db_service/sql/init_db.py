from main_app.db_config.postgres_conn import create_engine
from base_model import Base


# Initialize the engine and create all the tables
def init_db():
    engine = create_engine("postgresql://username:1234@localhost/ocean_vision")
    Base.metadata.create_all(engine)