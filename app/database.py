# SQLAlchemy la irunthu database engine create panna
from sqlalchemy import create_engine
# Database connection URL-a properly create panna
from sqlalchemy.engine import URL

# Database session create panna
# DeclarativeBase -> SQLAlchemy models-ku base class
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Namma project config.py la irukkura settings-a import panrom
# Database username, password, host, database name etc. inga irukkum
from app.config import settings


# Database connection URL create panrom
# Indha values ellam config.py la irukkura settings la irunthu varum
DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username=settings.DB_USER,
    password=settings.DB_PASSWORD,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    database=settings.DB_NAME,
    query={
        "charset" : "utf8mb4"
    }
)



# Indha engine moolama SQLAlchemy
# MySQL database-oda connection-a manage pannum
engine = create_engine(DATABASE_URL)


# Database session create panna sessionmaker use panrom
# bind=engine -> indha session namma database engine-a use pannum
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


# Namma SQLAlchemy models ellam
# indha Base class-a inherit pannum
class Base(DeclarativeBase):
    pass


# FastAPI endpoint-ku database session provide panna
# indha dependency function use pannuvom
def get_db():
    # Oru new database session create panrom
    db = SessionLocal()

    try:
        # Endpoint-ku database session-a provide panrom
        yield db

    finally:
        # Request mudinjathukku piragu
        # database session-a close panrom
        db.close()