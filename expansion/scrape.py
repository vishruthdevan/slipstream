import json
import random
import time
import traceback

import requests
from bs4 import BeautifulSoup, Tag
from googlesearch import search

INPUT_FILE = "circuits.txt"
OUTPUT_FILE = "circuit_links.json"
USER_AGENTS = [
    # Chrome
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
    # Firefox
    "Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
    "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)",
]


def get_wikipedia_link(query):
    for url in search(query + " site:wikipedia.org", num_results=5):
        if "wikipedia.org" in url:
            return url
    return None


def get_intro_paragraphs(url):
    try:
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        res = requests.get(url, headers=headers)
        if res.status_code == 429:
            print(res.headers)
            time.sleep(int(res.headers["Retry-After"]))

        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        content_div = soup.find("div", class_="mw-content-ltr mw-parser-output")
        if not content_div:
            return None

        intro_paragraphs = []

        for element in content_div.children:
            if element.name == "div" and "mw-heading" in element.get("class", []):
                break  # Stop at first heading div

            if element.name == "p":
                for sup in element.find_all("sup"):
                    sup.decompose()

                text = element.get_text(separator=" ", strip=True)
                print(text)
                if text:
                    intro_paragraphs.append(text)

        return "\n\n".join(intro_paragraphs) if intro_paragraphs else None

    except Exception as e:
        print(f"Failed to fetch intro from {url}: {e}")
        return None


def main():
    with open(INPUT_FILE, "r") as f:
        circuit_names = [line.strip() for line in f if line.strip()]

    data = {}

    for name in circuit_names:
        print(f"\nSearching for: {name}")
        try:
            link = get_wikipedia_link(name)
            if not link:
                print("No Wikipedia link found.")
                data[name] = {"url": None, "intro": None}
                continue

            print(f"Found: {link}")
            intro = get_intro_paragraphs(link)
            if intro:
                print(f"Intro snippet: {intro}...")
            else:
                print("No intro section found.")

            data[name] = {"url": link, "intro": intro}

        except Exception as e:
            print(f"Error processing {name}: {e}")
            data[name] = {"url": None, "intro": None}

        time.sleep(1)  # Rate-limit Google politely

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\nSaved results to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
