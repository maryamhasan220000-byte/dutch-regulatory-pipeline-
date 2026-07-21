import os
from dotenv import load_dotenv
from sqlalchemy import create_engine 
from models import Base 

load_dotenv()

db_user = os.getenv('AZURE_DB_USER')
db_password = os.getenv('AZURE_DB_PASSWORD')
db_host = os.getenv('AZURE_DB_HOST')
db_port = os.getenv('AZURE_DB_PORT')
db_name = os.getenv('AZURE_DB_NAME')

connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?sslmode=require"
engine = create_engine(connection_string)
Base.metadata.create_all(engine)
print("Tables created on AZURE database")

