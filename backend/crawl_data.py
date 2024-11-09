import os
import requests
import json
import uuid  # For generating unique random filenames
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

# Set the CORE API key from .env file
CORE_API_KEY = os.getenv('CORE_API_KEY')
BASE_URL = 'https://api.core.ac.uk/v3'

def fetch_data(endpoint, params=None):
    """
    Fetches data from the specified CORE API endpoint.
    
    Args:
        endpoint (str): The endpoint of the API to call.
        params (dict): Optional dictionary of parameters to include in the request.
        
    Returns:
        dict: The JSON response from the API as a dictionary.
    """
    headers = {
        'Authorization': f'Bearer {CORE_API_KEY}'
    }
    response = requests.get(f'{BASE_URL}/{endpoint}', headers=headers, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        # Raise an error if the request was not successful
        response.raise_for_status()

def get_research_articles(query, num_articles=10):
    """
    Retrieves multiple research articles with selected metadata fields.
    
    Args:
        query (str): The search query (e.g., "machine learning").
        num_articles (int): The number of articles to retrieve.
        
    Returns:
        list of dict: A list of metadata dictionaries for each research article.
    """
    articles = []
    page = 1
    articles_per_page = min(num_articles, 10)  # Ensure the page size is within limits

    while len(articles) < num_articles:
        search_params = {
            'q': query,
            'page': page,
            'pageSize': articles_per_page
        }
        
        # Search for articles
        search_results = fetch_data('search/works', params=search_params)
        
        # Add each article's metadata to the list
        for result in search_results.get('results', []):
            article_id = result['id']
            article_data = fetch_data(f'works/{article_id}')
            
            # Extract specific fields
            title = article_data.get('title', 'No title available')
            authors = [author.get('name', 'Unknown') for author in article_data.get('authors', [])]
            year = article_data.get('year', 'No year available')
            abstract = article_data.get('abstract', 'No abstract available')
            full_text = article_data.get('fullText', 'No full text available')
            full_text_link = article_data.get('downloadUrl', 'No link available')
            keywords = article_data.get('keywords', 'No keywords available')
            publisher = article_data.get('publisher', 'No publisher available')
            publication_date = article_data.get('publicationDate', 'No publication date available')
            journal = article_data.get('journal', {}).get('name', 'No journal available')
            citation_count = article_data.get('citationCount', 'No citation count available')
            
            # Format the article data
            article_metadata = {
                "Title": title,
                "Authors": ", ".join(authors),
                "Year": year,
                "Abstract": abstract,
                "Keywords": keywords,
                "Publisher": publisher,
                "Publication Date": publication_date,
                "Journal": journal,
                "Citation Count": citation_count,
                "Full Text": full_text,
                "Link": full_text_link
            }
            articles.append(article_metadata)

            # Stop if we have collected the desired number of articles
            if len(articles) >= num_articles:
                break
        
        page += 1  # Move to the next page of results if needed

    return articles

def save_metadata_to_file(data):
    """
    Saves the article metadata to a JSON file with a random unique filename.
    
    Args:
        data (dict): The article metadata.
    """
    # Generate a unique random filename
    filename = f"raw_data/{uuid.uuid4()}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    os.makedirs('raw_data', exist_ok=True)  # Ensure raw_data directory exists
    queries = ["Python"]

    for query in queries:
        articles = get_research_articles(query, num_articles=10)  # Retrieve 10 articles for each query
        for article in articles:
            save_metadata_to_file(article)