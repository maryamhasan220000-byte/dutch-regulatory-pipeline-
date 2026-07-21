from email.utils import parsedate_to_datetime
from datetime import datetime, timezone
import html
from bs4 import BeautifulSoup
from logger import get_logger

logger = get_logger(__name__)

def parse_pub_date(pub_date_string: str | None) -> "datetime | None":
    if pub_date_string is None:
        return None
    try: 
        parsed = parsedate_to_datetime(pub_date_string)
    except (TypeError, ValueError):
        return None 
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed 

def clean_description(raw_description: str |None)-> str | None:
    if raw_description is None:
        return None
    unescaped = html.unescape(raw_description)
    soup = BeautifulSoup(unescaped, 'html.parser')
    clean_text = soup.get_text()
    return clean_text.strip()

def validate_publications(publications: dict) -> bool:
    title = publications.get('title')
    link = publications.get('link')
    guid = publications.get('guid')
    if title is None or title.strip() == '':
        logger.warning(f"Discarding publication with missing title. Link {link}")
        return False 
    if link is None or link.strip() == '':
        logger.warning(f"Discarding publication with missing link. Title{title}")
        return False
    if guid is None or guid.strip() == '':
        logger.warning(f"Discarding publication with missing guid. Title {title}")
        return False
    if publications.get('pub_date') is None:
        logger.warning(f"Publication has no pub_date, but keeping it anyway. Title {title}")
    return True
def proccess_publication(raw_publication: dict, language: str) -> dict | None:
    cleaned_publication = clean_description(raw_publication.get('description'))
    parsed_pub_date = parse_pub_date(raw_publication.get('pub_date'))
    candidate = {
        'source' : raw_publication.get('source'),
        'guid': raw_publication.get('guid'),
        'link': raw_publication.get('link'),
        'title': raw_publication.get('title'),
        'description': cleaned_publication,
        'pub_date': parsed_pub_date,
        'language': language,
    }
    if not validate_publications(candidate):
        return None
    candidate['fetched_at'] = datetime.now(timezone.utc)
    return candidate
def process_all_publications(raw_publications: list[dict], language_map: dict) -> list[dict]:
    clean_publications =[]
    for raw_publication in raw_publications:
        source = raw_publication.get('source')
        language = language_map.get(source, 'unknown')
        processed = proccess_publication(raw_publication, language)
        if processed is not None:
            clean_publications.append(processed)
    logger.info(
        f"Processed {len(raw_publications)} raw publications"
        f"{len(clean_publications)} passed validation"
    )
    return clean_publications

 