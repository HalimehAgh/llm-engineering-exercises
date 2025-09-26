# website.py
import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from openai import OpenAI

load_dotenv()  # read .env

API_KEY = os.getenv("OPENAI_API_KEY")

def make_openai_client(api_key=None):
    if api_key is None:
        api_key = API_KEY
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set. Create a .env file or set the env var.")
    return OpenAI(api_key=api_key)

HEADERS = {
    "User-Agent": "llm-exercises/1.0 (+https://github.com/HalimehAgh/llm-engineering-exercises.git)"
}

class Website:
    def __init__(self, url, headers=None):
        self.url = url
        self.headers = headers or HEADERS
        resp = requests.get(url, headers=self.headers, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.content, "html.parser")
        self.title = soup.title.string.strip() if soup.title and soup.title.string else "No title found"
        # Remove common irrelevant elements
        if soup.body:
            for tag in soup.body(["script", "style", "img", "input", "nav", "footer", "header"]):
                tag.decompose()
            self.text = soup.body.get_text(separator="\n", strip=True)
        else:
            self.text = soup.get_text(separator="\n", strip=True)

def build_messages(website: Website, system_prompt=None):
    system_prompt = system_prompt or (
        "You are an assistant that analyzes the contents of a website and provides a short summary "
        "in Markdown. Ignore navigation, repeated footer/copyright, and inline ads. If there are "
        "news or announcements, summarize those too."
    )
    user_content = f"Website title: {website.title}\n\nContent:\n{website.text}"
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content}
    ]

def summarize_url(url: str, client: OpenAI = None, model: str = "gpt-4o-mini"):
    """
    Returns text summary (string).
    Accepts optional OpenAI client for testing or custom settings.
    """
    website = Website(url)
    client = client or make_openai_client()
    messages = build_messages(website)
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.0
    )
    # SDK returns choices with message field
    return resp.choices[0].message.content
