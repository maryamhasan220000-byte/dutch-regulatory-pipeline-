import json
from fetcher import fetch_all_feeds
from processor import process_all_publications
from storage import save_new_publications 
from logger import get_logger 

logger = get_logger(__name__)

def load_config()-> dict:
    with open('config.json', 'r') as f:
        return json.load(f)

def build_language_map(config: dict)-> dict:
    language_map ={}
    for source in config['sources']:
        language_map[source['name']] = source['language']
    return language_map 

def run_pipeline():
    logger.info("Pipeline starting")
    config = load_config()
    language_map = build_language_map(config)
    raw_publications = fetch_all_feeds(config)
    clean_publications = process_all_publications(raw_publications, language_map)
    new_count = save_new_publications(clean_publications)
    logger.info(f"Pipeline completed. {new_count} new publications saved")

if __name__ == '__main__':
    run_pipeline()