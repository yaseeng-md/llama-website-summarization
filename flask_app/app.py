from flask import Flask, request, jsonify
from utils import search_articles, fetch_article_content, concatenate_content, generate_answer

# Load environment variables from .env file
app = Flask(__name__)


@app.route('/query', methods=['POST'])
def query():
    """
    Handles the POST request to '/query'. Extracts the query from the request,
    processes it through the search, concatenate, and generate functions,
    and returns the generated answer.
    """
    # Get the data/query from streamlit app
    data = request.get_json()  # Retrieve JSON data sent by the client
    query = data.get("query", "")  # Extract the query from the JSON data
    print("Received query: ", query)

    # Step 1: Search and scrape articles based on the query
    print("Step 1: Searching articles")
    articles = search_articles(query=query)

    # Step 2: Concatenate content from the scraped articles
    print("Step 2: Concatenating content")
    concat = concatenate_content(articles=articles)

    # Step 3: Generate an answer using the LLM
    print("Step 3: Generating answer")
    answer = generate_answer(content=concat, query=query)

    # Return the jsonified answer back to Streamlit
    return jsonify({"answer": answer})


if __name__ == '__main__':
    app.run(host='localhost', port=5001)
