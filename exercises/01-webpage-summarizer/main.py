# main.py
import argparse
from website import summarize_url

def main():
    parser = argparse.ArgumentParser(description="Summarize a webpage using OpenAI")
    parser.add_argument("url", help="URL to summarize (e.g. https://example.com)")
    parser.add_argument("--model", default="gpt-4o-mini", help="OpenAI model to use")
    args = parser.parse_args()

    try:
        summary = summarize_url(args.url, model=args.model)
        print(summary)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
