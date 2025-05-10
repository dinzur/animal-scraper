# 🐾 Animal Collateral Adjective Scraper

This Python project scrapes the Wikipedia page for animal names and their **collateral adjectives**, downloads an image for each animal, and generates a clean, categorized HTML report.

## 🧠 Features

- Extracts all animals and their collateral adjectives from [Wikipedia](https://en.wikipedia.org/wiki/List_of_animal_names)
- Supports multiple adjectives per animal
- Downloads images to `/tmp/`
- Displays animals with images in an HTML report grouped by adjective
- Uses **threading** to speed up downloads
- Clean, modular, production-style code
- Includes test coverage

## 📁 Project Structure

├── src/
│ ├── main.py # Entry point
│ ├── scraper.py # Wikipedia scraping logic
│ ├── image_downloader.py # Image download logic
│ ├── html_generator.py # HTML report generator
│ ├── utils.py # Shared helpers
├── tests/
│ ├── test_scraper.py
│ ├── test_image_downloader.py
├── requirements.txt
├── README.md


## 🚀 How to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the scraper
python -m src.main
```

The report will be saved to: output/report.html
Images are saved to: /tmp/

## 🧪 Running Tests
```bash
python -m unittest discover -s tests
```

## ⏱️ Time Spent
Total: ~6.5 hours
Wikipedia parsing: 1.5h
Image scraping & fallback logic: 3h
HTML generation: 0.5h
Threading & concurrency: 0.5h
Testing & validation: 1h

## 🔍 Future Improvements
* Retry failed image downloads from log
* Support alternative image sources (e.g. Wikimedia API)
* Cache results to avoid re-downloading
* Add CLI arguments for custom paths or filters

## 🧰 Dependencies
requests
beautifulsoup4