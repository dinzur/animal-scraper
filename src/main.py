from scraper import extract_adjective_animal_map
from image_downloader import download_images_multithreaded
from html_generator import generate_html

def main():
    """
    Main entry point: Scrapes data, downloads images, and generates an HTML report.
    """
    
    print("Extracting data from Wikipedia...")
    adjective_map = extract_adjective_animal_map()

    print("Downloading images...")
    image_map = download_images_multithreaded(adjective_map)

    print("Generating HTML report...")
    generate_html(adjective_map, image_map)

    print("Done! Check output/report.html")

if __name__ == "__main__":
    main()
