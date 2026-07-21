import pytest
from processor import parse_pub_date , validate_publications, clean_description, proccess_publication, process_all_publications

def test_parse_pub_date():
    result = parse_pub_date('Wed, 08 Jul 2026 10:00:00 Z')
    assert result.year == 2026
    assert result.month == 7
    assert result.day == 8

@pytest.fixture
def valid_publications():
    return{
        'source': 'AFM',
        'guid': '{ABC-123}',
        'title': 'AFM publiceert nieuwe richtlijen',
        'link': 'https://www.afm.nl/article-1',
        'description': None,
        'pub_date': 'Wed, 08 Jul 2026 10:00:00 Z'

        
    }

def test_validate_publication_valid(valid_publications):
    result = validate_publications(valid_publications)
    assert result is True 

def test_validate_publication_missing_title(valid_publications):
    valid_publications['title'] = None 
    result = validate_publications(valid_publications)
    assert result is False

def test_validate_publication_missing_guid(valid_publications):
    valid_publications['guid'] = ''
    result = validate_publications(valid_publications)
    assert result is False 

def test_clean_description_strips_html():
    raw = '&lt;p&gt;De mavrow ik hebjn.&lt;/p&gt;'
    result = clean_description(raw)
    assert result == 'De mavrow ik hebjn.'

def test_clean_description_none():
    result = clean_description(None)  
    assert result is None

def test_clean_description_empty_string():
    result = clean_description('')
    assert result == ''

def test_process_publication_valid(valid_publications):
    result = proccess_publication(valid_publications, language='nl')

    assert result is not None 
    assert result['source'] == 'AFM'
    assert result['language'] == 'nl'
    assert 'fetched_at' in result 


def test_process_all_publications_mixed():
    raw_publication = [
        {'source': 'DNB', 'guid': 'https://dnb.nl/a', 'title': 'Valid DNB item',
         'link': 'https://dnb.nl/a', 'description': None, 'pub_date': 'Wed, 08 Jul 2026 10:00:00 GMT'},
        {'source': 'AFM', 'guid': '{abc-123}', 'title': None,
         'link': 'https://afm.nl/b', 'description': None, 'pub_date': 'Tue, 07 Jul 2026 09:00:00 Z'},
    
    ]
    language_map = {'DNB': 'en', 'AFM': 'nl'}

    result = process_all_publications(raw_publication, language_map)
    assert len(result) ==1
    assert result[0]['source'] == 'DNB'

def test_process_all_publications_empty_input():
    result = process_all_publications([], {'DNB': 'en', 'AFM': 'nl'})
    assert result == []

