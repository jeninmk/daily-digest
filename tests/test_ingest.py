from digest.ingest import fetch_feed

SAMPLE_RSS = """<?xml version="1.0"?>
<rss version="2.0"><channel><title>Test</title>
<item><title> Hello World </title><link>http://x/1</link>
<pubDate>Mon, 01 Jan 2024 00:00:00 GMT</pubDate></item>
<item><title>No link, skipped</title></item>
</channel></rss>"""


def test_fetch_feed_parses_entries():
    articles = fetch_feed("Test", SAMPLE_RSS, "news")
    assert len(articles) == 1
    a = articles[0]
    assert a.title == "Hello World"  # stripped
    assert a.url == "http://x/1"
    assert a.source == "Test"
    assert a.interest == "news"
    assert a.published is not None
