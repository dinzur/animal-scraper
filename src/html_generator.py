import os
from utils import clean_animal_name

def generate_html(adjective_map, image_map, output_file="output/report.html"):
    """
    Generate a categorized HTML report showing animals grouped by collateral adjective,
    along with their downloaded images.
    Args:
        adjective_map (dict): Mapping of adjective → list of animals.
        image_map (dict): Mapping of cleaned animal name → image file path.
        output_file (str): Output path to write the HTML file.
    """

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        # Write HTML and styling boilerplate
        f.write("""
        <html><head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Animal Collateral Adjectives</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #f0f2f5; }
            h1 { text-align: center; }
            h2 { margin-top: 40px; color: #333; }
            .grid { display: flex; flex-wrap: wrap; gap: 20px; }
            .card {
                background: white;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                padding: 10px;
                width: 180px;
                text-align: center;
            }
            .card img {
                max-width: 100%;
                height: 120px;
                object-fit: cover;
                border-radius: 4px;
            }
        </style>
        </head><body>
        <h1>Animal Collateral Adjectives</h1>
        """)

        # For each adjective (e.g., 'bovine', 'canine'), render a section
        for adjective in sorted(adjective_map.keys()):
            f.write(f"<h2>{adjective.capitalize()}</h2><div class='grid'>")
            for animal in sorted(adjective_map[adjective]):
                clean_name = clean_animal_name(animal)
                img_path = image_map.get(clean_name)

                if img_path and os.path.exists(img_path):
                    # Use a relative path to ensure images are loaded by browser
                    relative_path = os.path.relpath(img_path, start=os.path.dirname(output_file))
                    img_tag = f'<img src="{relative_path}" alt="{animal}"/>'
                else:
                    # If image is missing, show a placeholder
                    img_tag = '<div style="height:120px; background:#ccc;"></div>'

                f.write(f"<div class='card'>{img_tag}<div>{animal}</div></div>")
            f.write("</div>")

        f.write("</body></html>")
