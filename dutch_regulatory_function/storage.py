import os 
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from models import Base, Publication
from logger import get_logger 

logger = get_logger(__name__)

def get_session():
    load_dotenv()

    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')

    connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?sslmode=require"
    engine = create_engine(connection_string)
    Base.metadata.create_all(engine)

    SessionFactory = sessionmaker(bind=engine)
    return SessionFactory()

def save_new_publications(clean_publications: list[dict])-> int:
    session = get_session()
    new_count = 0
    try:
        for pub_dict in clean_publications:
            guid = pub_dict['guid']
            already_exists = session.query(Publication).filter_by(guid=guid).first()
            if already_exists is not None:
                continue 
            new_publication = Publication(**pub_dict)
            session.add(new_publication)
            new_count += 1
        session.commit()
        logger.info(f"Saved {new_count} new publications out of {len(clean_publications)} processed")
    except Exception as e:
        session.rollback()
        logger.error(f" Storage failed, rolling back entire transcation: {e}")
    finally:
        session.close()
    return new_count

            