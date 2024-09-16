import os
import time
import asyncio
from csv_writer import write_csv
from env_loader import load_env_file
from text_editors import translate_all_news
from parser_functions import get_page_html, parse_news


# Loading environment variables
load_env_file()


async def main():
    """
    The main asynchronous function that handles scraping, parsing, translating,
    and writing news data to a CSV file.

    It scrapes news articles from multiple pages, translates their content, 
    and writes the original and translated content to a CSV file. The execution 
    time is measured to evaluate the performance.
    """

    # Start the timer to measure total execution time
    start_time = time.time()
    
    # List to store all news articles across multiple pages
    # all_news = []

    start_page = int(os.getenv("START_PAGE"))
    end_page = int(os.getenv("END_PAGE"))
    news_category = os.getenv("NEWS_CATEGORY")

    # Loop through the first 2 pages of the 'economy-trade' category
    for page in range(start_page, end_page):
        # Fetch and parse the HTML content of the page
        html = get_page_html(page, news_category)
        response = parse_news(html)
        write_csv(response, "data/results.csv")

        # Add the parsed news articles to the overall list
        # all_news.extend(response)
        print(f"The data from the page {page} is collected")

    # Asynchronously translate all the news articles (short and main text)
    # translated_news = await translate_all_news(all_news)

    # Write the translated news data to a CSV file
    # write_csv(translated_news, "data/results.csv")
    
    # End the timer and print the execution time
    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.2f} sec")


if __name__ == "__main__":
    asyncio.run(main())