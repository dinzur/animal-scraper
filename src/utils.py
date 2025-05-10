import re

def safe_filename(name: str) -> str:
    """
    Convert a string into a safe filename by replacing unsafe characters.
    Args:
        name (str): The original string.
    Returns:
        str: A sanitized filename string.
    """

    return re.sub(r'[^a-zA-Z0-9_-]', '_', name)

def clean_animal_name(name: str) -> str:
    """
    Normalize an animal name by removing citations, parentheses, and unrelated notes.
    Args:
        name (str): Raw animal name text.
    Returns:
        str: Cleaned animal name.
    """

    name = re.sub(r"\s*\(.*?\)", "", name)
    name = re.sub(r"\[.*?\]", "", name)
    name = re.split(r'Also see|See also', name, flags=re.IGNORECASE)[0]
    return name.strip()

import requests

def search_wikipedia_title(query):
    """
    Uses Wikipedia's API to search for a page title related to the query.
    Returns the best-matching page title or None if not found.
    """
    try:
        params = {
            'action': 'query',
            'list': 'search',
            'srsearch': query,
            'format': 'json'
        }
        r = requests.get("https://en.wikipedia.org/w/api.php", params=params)
        r.raise_for_status()
        results = r.json().get('query', {}).get('search', [])
        if results:
            return results[0]['title']
    except Exception as e:
        print(f"[WARN] Wikipedia search API failed: {e}")
    return None

