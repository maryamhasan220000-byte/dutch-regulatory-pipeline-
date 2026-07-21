import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
db_user = os.getenv('AZURE_DB_USER')
db_password = os.getenv('AZURE_DB_PASSWORD')
db_host = os.getenv('AZURE_DB_HOST')
db_port = os.getenv('AZURE_DB_PORT')

connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/postgres?sslmode=require"

engine = create_engine(connection_string)
with engine.connect() as connection:
    connection.execute(text("COMMIT"))
    connection.execute(text("CREATE DATABASE dutch_regulatory"))
    print("DATABASE dutch_regulatory created on Azure")
    