# tests/test_summarizer.py
from types import SimpleNamespace
import requests
import website

class FakeResponse:
    def __init__(self, html):
        self.status_code = 200
        self.content = html.encode("utf-8")
    def raise_for_status(self):
        pass

def test_website_parsing(monkeypatch):
    html = "<html><head><title>Test</title></head><body><p>Hello world</p></body></html>"
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: FakeResponse(html))
    w = website.Website("https://edition.cnn.com/")
    assert "Hello world" in w.text
    assert w.title == "Test"

def test_summarize_inject_fake_client(monkeypatch):
    # patch requests.get to return simple HTML
    html = "<html><head><title>Test</title></head><body><p>Some paragraph</p></body></html>"
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: FakeResponse(html))

    # create fake client with expected shape
    def fake_create(*args, **kwargs):
        return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content="FAKE SUMMARY"))])

    fake_client = SimpleNamespace()
    fake_client.chat = SimpleNamespace()
    fake_client.chat.completions = SimpleNamespace(create=fake_create)

    out = website.summarize_url("https://edition.cnn.com/", client=fake_client)
    assert out == "FAKE SUMMARY"
