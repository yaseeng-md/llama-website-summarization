import os
import dotenv
import requests
from openai import OpenAI
from bs4 import BeautifulSoup


# Load API keys from environment variables
# Change the path of the .env files while running the code.
dotenv.load_dotenv(r"C:\Users\gandl\Documents\Deep edge Assignment\.env")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)


def search_articles(query):
    """
    Searches for articles related to the query using Serper API.
    Returns a list of dictionaries containing article URLs, headings, and text.

    SERPER API Returns the following in dictionary, mainly consists
    1. Search parameters -> key = "searchParameters",
        which contains query("q"), Country ("gl"), Language("hl"), status of autocorrect("autocorrect").
    2. Knowledge Graph
    3. Organic("organic") -> This is the list of actual search result links (what you see in Google search listings),
        with Title of page (title), URL(link),Snippet that is on website(snippet)
    """

    # Taken from the official website of SERPER API.
    URL = "https://google.serper.dev/search"
    HEADERS = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "q": query
    }
    responces = requests.post(url = URL, headers = HEADERS, json = data)
    responces.raise_for_status()
    results = responces.json()

    articles = []
    # implement the search logic - retrieves articles
    # We are taking top 10 articles or web pages to analyze
    NUM_ARTICLES = 2
    for item in results.get("organic", [])[:NUM_ARTICLES]:
        title = item.get("title", "")
        link = item.get("link","")
        if title and link:
            # Create a dictionary of the title and link retried.
            articles.append({"title" : title, "link" : link})
    return articles


def fetch_article_content(url):
    """
    Fetches the article content, extracting headings and text.
    Parses heading with scraping tool Beautiful Soup, by accessing the tags [h1,h2,h3,h4] or [article] tag from website.
    """
    try:
        responce = requests.get(url, timeout=10)
        responce.raise_for_status()
    except requests.RequestException as e:
        print(f"[ERROR] Could not fetch URL: {url} -> {e}")
        return ""
    beautiul_soup = BeautifulSoup(responce.text, "html.parser")

    # We remove the following tags so that we can extract useful content.
    for tag in beautiul_soup(["script", "style", "nav", "footer", "form", "aside", "noscript", "header"]):
        tag.decompose()

    content = ""
    # implementation of fetching headings and content from the articles
    # Fetching all headings

    article = beautiul_soup.find("article") # check for article tag
    if article:
        elements = article.find_all(["h1", "h2", "h3", "p"])
    else:
        elements = beautiul_soup.find_all(["h1", "h2", "h3", "p"])

    for ele in elements:
        text = ele.get_text(strip=True)
        if text:
            content += text + "\n\n"

    return content.strip()


def concatenate_content(articles):
    """
    Concatenates the content of the provided articles into a single string.
    """
    full_text = ""
    # formatting + concatenation of the string is implemented here
    for i, article in enumerate(articles, 1):
        title = article.get("title", f"Article {i}")
        link = article.get("link", "")
        content = fetch_article_content(link)

        if content:
            full_text += f"\n\n=== {title} ===\n{content}\n"

    return full_text


def generate_answer(content, query):
    # Generate the Prompt to give it to client, and generate answers.
    """
    Client returns the response in a outline of :
    {
      "id": "chatcmpl-B9MBs8CjcvOU2jLn4n570S5qMJKcT",
      "object": "chat.completion",
      "created": 1741569952,
      "model": "gpt-4.1-2025-04-14",
      "choices": [
        {
          "index": 0,
          "message": {
            "role": "assistant",
            "content": "Hello! How can I assist you today?",
            "refusal": null,
            "annotations": []
          },
          "logprobs": null,
          "finish_reason": "stop"
        }
      ],
      "usage": {
        "prompt_tokens": 19,
        "completion_tokens": 10,
        "total_tokens": 29,
        "prompt_tokens_details": {
          "cached_tokens": 0,
          "audio_tokens": 0
        },
        "completion_tokens_details": {
          "reasoning_tokens": 0,
          "audio_tokens": 0,
          "accepted_prediction_tokens": 0,
          "rejected_prediction_tokens": 0
        }
      },
      "service_tier": "default"
    }

    """


    prompt = f"""
    Based on the following content, answer the query in a concise and informative manner:

    --- Content Start ---
    {content}
    --- Content End ---

    Query: {query}
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Used gpt-3.5-turbo, as I am using free tier of OpenAI API
            messages=[
                {"role": "system",
                 "content": "You are a helpful assistant that provides accurate information based on the given content."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        answer = response.choices[0].message.content
        return answer

    except Exception as e:
        print(f"[ERROR] OpenAI API call failed: {e}")
        return "An error occurred while generating the answer."


# --------------> Function for testing utils.py <--------------

# --------------> Test search_articles <--------------------
test_query = "Deep Edge, Hyderabad"
articles = search_articles(test_query)


print("------ Fetched Articles ------")
for a in articles:
    print(f"Title: {a['title']}")
    print(f"URL: {a['link']}\n")

# --------------> Test fetch_article_content <--------------------
# print("------ Fetched Content from First Article ------")
# first_url = articles[0]['link']
# content = fetch_article_content(first_url)
# print(content[:2000])

# --------------> Test concatenate_content <--------------------
full_text = concatenate_content(articles)
print("------ Concatenated Article Content ------")
print(len(full_text))

# --------------> Test generate_answer <--------------------
answer = generate_answer(full_text, test_query)
print("------ Generated Answer ------")
print(answer)

