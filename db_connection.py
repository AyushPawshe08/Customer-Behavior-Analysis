from sqlalchemy import create_engine

DATABASE_URL = "postgresql://postgres:fcbispassword@localhost:5432/"

engine = create_engine(DATABASE_URL)
