import datetime
import logging
import azure.functions as func

from fetcher import fetch_all_feeds
from processor import process_all_publications 
from storage import save_new_publications 

app = func.FunctionApp()

def load_config():
    import json 
    with open('config.json', 'r') as f:
        return json.load(f)

def build_language_map(config):
    language_map ={}
    for source in config['sources']:
        language_map[source['name']] = source['language']
    return language_map
@app.timer_trigger(schedule="0 0 6 * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False)
def RunPipeline(myTimer: func.TimerRequest)->None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()



    if myTimer.past_due:
        logging.info('The timer is past due!')
    logging.info(f'Dutch regulatory pipleine starting at {utc_timestamp}')
    config = load_config()
    language_map = build_language_map(config)
    raw_publications = fetch_all_feeds(config)
    clean_publications = process_all_publications(raw_publications, language_map)
    new_count = save_new_publications(clean_publications)
    logging.info(f'Pipeline complete. {new_count} new publications saved.')

        
