from unittest.mock import patch, Mock
from storage import save_new_publications 

def test_save_new_publications_skips_existing():
    clean_publications = [
        {'source': 'DNB', 'guid': 'https://dnb.nl/existing', 'title': 'Already seen',
         'link': 'https://dnb.nl/existing', 'description': None, 'pub_date': None,
         'language': 'en', 'fetched_at': None},
    ]

    with patch('storage.get_session') as mock_get_session:
        mock_session = Mock()
        mock_session.query.return_value.filter_by.return_value.first.return_value = Mock()
        mock_get_session.return_value = mock_session

        new_count = save_new_publications(clean_publications)
    assert new_count == 0
    mock_session.add.assert_not_called() 

def test_save_new_publications_saves_new()   :
    clean_publications = [
        {'source': 'DNB', 'guid': 'https://dnb.nl/new', 'title': 'Genuinely new',
         'link': 'https://dnb.nl/new', 'description': None, 'pub_date': None,
         'language': 'en', 'fetched_at': None},
    ]   

    with patch('storage.get_session') as mock_get_session:
        mock_session = Mock()
        mock_session.query.return_value.filter_by.return_value.first.return_value = None
        mock_get_session.return_value = mock_session

        new_count = save_new_publications(clean_publications)

    assert new_count == 1
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
