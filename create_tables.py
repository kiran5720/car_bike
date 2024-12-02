from sqlalchemy import create_engine
from models import Base  # import the Base from models.py


# Database connection URL (PostgreSQL example)
DATABASE_URL = "postgresql://postgres:admin@localhost:5432/car_bike"

# Create the engine and tables
engine = create_engine(DATABASE_URL)

# Create all tables
Base.metadata.create_all(engine)
print("Tables created successfully.")

# from sqlalchemy import create_engine

# DATABASE_URL = "postgresql://username:password@localhost:5432/rental_db"
# engine = create_engine(DATABASE_URL)

# # Test connection
# with engine.connect() as connection:
#     print("Connected to the database!")

