import time 
import requests
from playwright.sync_api import sync_playwright 
import xml.etree.ElementTree as ET 
from logger import get_logger
from blob.storage import upload_raw_xml

logger = get_logger(__name__)

def fetch_feed(source_config: dict, request_config: dict)-> list[dict]:
    source_name = source_config['name']
    feed_url = source_config['feed_url']

    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "Accept": "application/rss+xml, application/xml;q=0.9, */*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9"
}
    
    timeout = request_config['timeout_seconds']

    logger.info(f"Fetching feed:{source_name}")
    try:
        with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)

                page = browser.new_page(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
    )

                response = page.goto(feed_url, wait_until="domcontentloaded", timeout=30000)

                xml_content = response.text()

                browser.close()
                upload_raw_xml(source_name=source_name, raw_xml=xml_content)

        #print(xml_content[:500])

        root: ET.Element[str] = ET.fromstring(xml_content)
       

             
              
             
             
        
    except Exception as e:
        logger.error(f"Failed to fetch {source_name}: {e}")
        return []
    
    channel = root.find('channel')
    if channel is None:
        logger.error(f"No <channel> element found in {source_name} feed")
        return []
    items = channel.findall('item')
    raw_publications = []

    for item in items:
        title_el = item.find('title')
        link_el = item.find('link')
        description_el = item.find('description')
        pub_date_el = item.find('pubDate')
        guid_el = item.find('guid')

        title = title_el.text if title_el is not None else None
        link = link_el.text if link_el is not None else None
        description = description_el.text if description_el is not None else None
        pub_date = pub_date_el.text if pub_date_el is not None else None
        guid = guid_el.text if guid_el is not None else link
        raw_publications.append({
            'source': source_name,
            'guid': guid,
            'title': title,
            'link': link,
            'description': description,
            'pub_date': pub_date
        })
        logger.info(f"Fetched {len(raw_publications)} items for {source_name}")
        
    return raw_publications

def fetch_all_feeds(config: dict) -> list[dict]:
    all_publications= []
    for source_config in config['sources']:
        publications = fetch_feed(source_config, config['request'])
        all_publications.extend(publications)
    logger.info(f"Total publications fetched across all sources: {len(all_publications)}")
    return all_publications 



