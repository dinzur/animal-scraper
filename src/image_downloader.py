import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, unquote
from utils import safe_filename, clean_animal_name

# Base URL for Wikipedia articles
WIKI_PAGE_URL = "https://en.wikipedia.org/wiki/"

# Directory where images will be saved (as per assignment: /tmp)
IMAGE_DIR = os.path.abspath("output/tmp")

def try_scrape_image(clean_name, original_name, tried_pages=None):
    """
    Attempt to scrape an animal image from Wikipedia using the given name.
    Recursively follows relevant internal links if the main page is a disambiguation or lacks images.
    Args:
        clean_name (str): A cleaned Wikipedia article title for the animal.
        original_name (str): The original raw name for logging purposes.
        tried_pages (set): A set of already-tried page titles to prevent cycles.
    Returns:
        str or None: Path to the downloaded image file, or None if unsuccessful.
    """

    # Keep track of visited pages to avoid infinite recursion
    tried_pages = tried_pages or set()
    title = quote(clean_name.replace(" ", "_"))
    if title in tried_pages:
        return None
    tried_pages.add(title)

    url = WIKI_PAGE_URL + title
    print(f"[INFO] Trying to scrape image for '{original_name}' from {url}")

    try:
        # Request the Wikipedia page
        resp = requests.get(url, allow_redirects=True)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')

        # Skip disambiguation pages — these are ambiguous entries (e.g., "Jaguar")
        if soup.find("table", {"id": "disambigbox"}) or "may refer to:" in soup.text[:500]:
            raise Exception("Disambiguation page detected")

        # Try to find a taxonomy box specific to animals
        infobox = soup.find("table", class_="infobox biota")
        if not infobox:
            # Fall back to a generic infobox if no biota-specific box exists
            infobox = soup.find("table", class_="infobox")

        if infobox:
            # Make sure the box contains biological classification keywords
            if infobox and any(k in infobox.text for k in ["Kingdom", "Phylum", "Species"]):
                images = infobox.find_all("img")
                if images:
                    return download_and_save_image(images[0], original_name)

        # If no usable image found in infobox, follow first relevant internal link
        content = soup.find("div", {"class": "mw-parser-output"})
        if content:
            for link in content.find_all("a", href=True):
                href = link["href"]
                title = link.get("title", "").lower()

                # Only follow links that are likely animal-related and not internal/page jumps
                if (
                    href.startswith("/wiki/")
                    and not any(x in href for x in [":", "#", "Main_Page"])
                    and any(animal_word in title for animal_word in ["animal", "bird", "mammal", "fish", "species", "genus"])
                ):
                    next_title = unquote(href.replace("/wiki/", "")).replace("_", " ")
                    return try_scrape_image(next_title, original_name, tried_pages)

        # If no usable content found at all, raise error
        raise Exception("No usable image found")

    except Exception as e:
        print(f"[WARN] Scraping failed for {original_name}: {e}")
        return None

def download_and_save_image(img, name):
    """
    Download an image from its <img> tag and save it locally to /tmp/.
    Args:
        img (Tag): BeautifulSoup <img> tag with a relative src.
        name (str): Animal name (used as filename).
    Returns:
        str: Full path to the saved image file.
    """

    # Extract full image URL
    img_url = "https:" + img["src"]
    img_data = requests.get(img_url).content

    # Ensure /tmp/ directory exists
    os.makedirs(IMAGE_DIR, exist_ok=True)

    # Create sanitized filename and save image bytes to disk
    filename = os.path.join(IMAGE_DIR, f"{safe_filename(name)}.jpg")
    with open(filename, "wb") as f:
        f.write(img_data)

    return filename

def download_image(animal_name):
    """
    Attempt to download an image for the given animal using name fallbacks.
    Args:
        animal_name (str): Raw animal name.
    Returns:
        str or None: Path to image file or None if all attempts failed.
    """

    clean_name = clean_animal_name(animal_name)

    # First try: the cleaned name
    result = try_scrape_image(clean_name, animal_name)
    if result:
        return result

    # Second try: if name contains slash (e.g., "ass/donkey"), try each part
    if '/' in animal_name:
        parts = [part.strip() for part in animal_name.split('/')]
        for part in parts:
            alt_name = clean_animal_name(part)
            result = try_scrape_image(alt_name, animal_name)
            if result:
                return result

    # Third try: fallback to just the first word
    first_word = clean_name.split()[0]
    if first_word != clean_name:
        result = try_scrape_image(first_word, animal_name)
        if result:
            return result

    # All fallbacks failed
    print(f"[ERROR] Could not get image for {animal_name}")
    return None

def download_images_multithreaded(adjective_map):
    """
    Download images for all unique animals using multithreading.
    Args:
        adjective_map (dict): Dictionary of adjective → list of animals.
    Returns:
        dict: Mapping of cleaned animal names to image file paths.
    """

    from threading import Thread
    image_map = {}     # Final result: animal_name → image_path
    seen = set()       # Prevent downloading the same animal more than once
    threads = []
    success_counter = [0]  # Track how many images we successfully downloaded

    def worker(animal):
        result = download_image(animal)
        if result:
            image_map[clean_animal_name(animal)] = result
            success_counter[0] += 1

    # Start a thread for each unique animal
    for animals in adjective_map.values():
        for animal in animals:
            clean = clean_animal_name(animal)
            if clean not in seen:
                seen.add(clean)
                t = Thread(target=worker, args=(animal,))
                threads.append(t)
                t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    print(f"[INFO] Successfully downloaded {success_counter[0]} images.")
    return image_map
