import json
from unittest import mock

from linkedin_api.client import Client

# The two meta tags _fetch_metadata reads from LinkedIn's home page, which it parses with
# BeautifulSoup's "lxml" parser.
HOME_PAGE = """<!DOCTYPE html>
<html><head>
<meta name="applicationInstance" content='{"applicationUrn": "urn:li:application:x", "version": "1.2.3"}'>
<meta name="clientPageInstanceId" content="abc-123">
</head><body><p>Hello</p></body></html>"""


def test_fetch_metadata_reads_the_meta_tags():
    client = Client()
    with mock.patch("linkedin_api.client.requests.get") as get:
        get.return_value.text = HOME_PAGE
        client._fetch_metadata()
    assert client.metadata["clientApplicationInstance"] == json.loads(
        '{"applicationUrn": "urn:li:application:x", "version": "1.2.3"}'
    )
    assert client.metadata["clientPageInstanceId"] == "abc-123"


def test_fetch_metadata_without_the_meta_tags_leaves_metadata_empty():
    client = Client()
    with mock.patch("linkedin_api.client.requests.get") as get:
        get.return_value.text = "<html><head></head><body></body></html>"
        client._fetch_metadata()
    assert "clientApplicationInstance" not in client.metadata
    assert "clientPageInstanceId" not in client.metadata
