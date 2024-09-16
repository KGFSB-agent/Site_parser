import httpx
from selectolax.parser import HTMLParser
from dataclasses import dataclass, asdict


@dataclass
class NewsTitle:
    """
    A class to represent a news article with attributes such as title, date, 
    link, and text content.

    Attributes:
        title (str): The title of the news article.
        news_date (str): The publication date of the news article.
        news_href (str): The URL link to the news article.
        news_short_text (str): A short description or summary of the news article.
        news_main_text (str): The main content of the news article.
        news_short_text_translated (str): The translated short description of the news (default is empty).
        news_main_text_translated (str): The translated main content of the news (default is empty).
        country (str): The country of origin (default is "China").
        category (str): The category of the news (default is "economy-trade").
    
    news_short_text_translated and news_main_text_translated was removed
    """

    title: str
    news_date: str
    news_href: str
    news_short_text: str
    news_main_text: str
    country: str = "China"
    category: str = "economy-trade"


def get_page_html(page, category):
    """
    Fetches the HTML content of a news page from the China Briefing website for a specific category and page.

    Args:
        page (int): The page number to fetch. Page 1 has a different URL format than subsequent pages.
        category (str): The category of the news (e.g., 'economy-trade').

    Returns:
        HTMLParser: The parsed HTML content of the page.
    """
    if page == 1:
        url = f"https://www.china-briefing.com/news/category/{category}/"
    else:
        url = f"https://www.china-briefing.com/news/category/{category}/page/{page}"
    
    # Send a GET request to fetch the page content
    response = httpx.get(url)
    return HTMLParser(response.text)


def parse_news(html):
    """
    Parses the HTML content to extract news articles from the China Briefing website.

    Args:
        html (HTMLParser): The parsed HTML content of a news page.

    Returns:
        list: A list of dictionaries containing information about each news article, 
              including title, date, link, short text, and main text.
    """
    
    # Select all news articles on the page
    newses = html.css("div.briefing-news")

    results = []
    # Iterate over each news article on the page
    for news in newses:
        # Extract the link to the news article
        news_href=news.css_first("a").attributes.get('href')
        response = httpx.get(news_href)
        news_html = HTMLParser(response.text)

        # Extract the main content of the article
        news_inner_text = news_html.css_first("div.article-content.post-content")
        
        # Collect all <p> and <li> tags that contain the news main text
        news_texts = []
        text_p_li_elements = news_inner_text.css("p, li")
        
        # Add the text from each <p> or <li> tag to the list
        for element in text_p_li_elements:
            news_texts.append(element.text())
        
        # Join all the text elements into one string to represent the full article text
        full_text = " ".join(news_texts)

        # Create a new NewsTitle object with the extracted data
        new_news = NewsTitle(
            title=news.css_first("a").text(),  # Extract the title of the news
            news_date=news.css_first("time.entry-date").text(),  # Extract the date
            news_href=news.css_first("a").attributes.get('href'),  # Extract the link to the news
            news_short_text=news.css("p")[1].text(),  # Extract the short description of the article
            news_main_text=full_text  # Use the joined full text as the main content
        )

        # Convert the NewsTitle dataclass to a dictionary and add it to the results list
        results.append(asdict(new_news))
    return results
