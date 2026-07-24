from unittest.mock import patch, Mock
from fetcher import fetch_feed
from unittest.mock import patch, Mock, MagicMock


def test_fetch_feed_handles_network_failure():
    source_config = {'name': 'DNB', 'feed_url': 'https://fake-url.com'}
    request_config = {'user_agent': 'test', 'timeout_seconds': 10}

    fake_xml = '''<rss>
        <channel>
            <item>
                <title>Test publication</title>
                <link>https://www.dnb.nl/test-1</link>
                <description>Some text</description>
                <pubDate>Wed, 08 Jul 2026 10:00:00 GMT</pubDate>
            </item>
        </channel>
    </rss>'''

    with patch('fetcher.sync_playwright') as mock_playwright:
        mock_pw = MagicMock()
        mock_browser = MagicMock()
        mock_page = MagicMock()
        mock_response = MagicMock()
        mock_playwright.return_value.__enter__.return_value = mock_pw

        mock_pw.chromium.launch.return_value = mock_browser
        mock_browser.new_page.return_value = mock_page

        mock_page.goto.return_value = mock_response
        mock_response.text.return_value = fake_xml
        

        result = fetch_feed(source_config, request_config)

    assert len(result) == 1
    assert result[0]['title'] == 'Test publication'
    assert result[0]['guid'] == 'https://www.dnb.nl/test-1'

    
        #mock_get.side_effect = requests.exceptions.RequestException("Connection failed")
        #result = fetch_feed(source_config, request_config)
        #assert result == []

