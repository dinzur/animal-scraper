import requests
import re
from bs4 import BeautifulSoup
from collections import defaultdict
from utils import clean_animal_name

WIKI_URL = "https://en.wikipedia.org/wiki/List_of_animal_names"

def clean_adjectives(text: str):
    """
    Clean and split a string of collateral adjectives into a list of lowercase strings.
    Args:
        text (str): Raw text from the adjective cell (may contain multiple adjectives and references).
    Returns:
        List[str]: A list of individual adjectives.
    """
    
    text = re.sub(r"\[.*?\]", "", text)
    return [adj.strip().lower() for adj in re.split(r"[;,/]| and ", text) if adj.strip()]

def fetch_wikipedia_table():
    """
    Fetch and parse the Wikipedia page containing animal name tables.
    Returns:
        BeautifulSoup: Parsed HTML soup of the page.
    """

    response = requests.get(WIKI_URL)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")

def extract_adjective_animal_map():
    """
    Extract a mapping of collateral adjectives to the animals that share them.
    Returns:
        dict: A dictionary where keys are adjectives and values are lists of animal names.
    """

    soup = fetch_wikipedia_table()
    tables = soup.find_all("table", class_="wikitable")
    adjective_map = defaultdict(list)

    for table in tables:
        headers = [th.text.strip().lower() for th in table.find("tr").find_all("th")]
        try:
            animal_idx = headers.index("animal")
            adj_idx = headers.index("collateral adjective")
        except ValueError:
            continue

        for row in table.find_all("tr")[1:]:
            cols = row.find_all("td")
            if len(cols) <= max(animal_idx, adj_idx):
                continue

            raw_animal = cols[animal_idx].text.strip()
            raw_adjective_parts = list(cols[adj_idx].stripped_strings)
            raw_adjectives = ' / '.join(raw_adjective_parts)

            animal = clean_animal_name(raw_animal)
            adjectives = clean_adjectives(raw_adjectives)

            for adj in adjectives:
                if animal not in adjective_map[adj]:
                    adjective_map[adj].append(animal)

    return adjective_map
