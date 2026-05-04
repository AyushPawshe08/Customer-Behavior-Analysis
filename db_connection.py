from sqlalchemy import create_engine


DATABASE_URL = "postgresql://YOUR_USERNAME:YOUR_PASSWORD@localhost:5432/customer_behavior"

engine = create_engine(DATABASE_URL)
