import os
import csv
from pathlib import Path


def write_csv(newses, csv_path):
    """
    Writes a dictionary with data about each news to a CSV file.

    Args:
        newses (dict): A dictionary with data about each news.
        csv_path (str): The file path for the CSV file.

    Returns:
        None
    
    news_short_text_translated and news_main_text_translated was removed
    """
    output_dir = Path(os.path.dirname(csv_path))
    output_dir.mkdir(parents=True, exist_ok=True)

    # Check if file already exists to avoid rewriting headers
    file_exists = os.path.exists(csv_path)

    headers = {
        "title": "Заголовок",
        "news_date": "Дата новости",
        "news_href": "Ссылка на новость",
        "news_short_text": "Краткое описание статьи",
        "news_main_text": "Основной текст новости",
        "country": "Страна",
        "category": "Категория"
    }
    
    with open(csv_path, "a", newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers.keys())

        # Write headers only if the file is newly created
        if not file_exists:
            writer.writeheader()
        
        writer.writerows(newses)