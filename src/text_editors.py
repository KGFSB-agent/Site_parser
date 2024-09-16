import asyncio
from deep_translator import GoogleTranslator


async def translate_text(text, target_lang="ru"):
    """
    Translates a given text into the target language.

    Args:
        text (str): The text to be translated.
        target_lang (str): The target language code (default is Russian).

    Returns:
        str: The translated text.
    
    If the text exceeds 5000 characters, it is split into chunks and translated sequentially.
    """
    try:
        # If the text is longer than 5000 characters, split it into chunks
        if len(text) > 5000:
            chunks = split_text(text, 5000)

            # Translate each chunk and join the translated parts
            translated_chunks = [GoogleTranslator(source="auto", target=target_lang).translate(chunk) for chunk in chunks]
            return " ".join(translated_chunks)
        else:
            # Translate the text directly if it's less than 5000 characters
            return GoogleTranslator(source="auto", target=target_lang).translate(text)
        
    except Exception as e:
        print(f"Error translating text: {e}")
        return text


def split_text(text, max_length=5000):
    """
    Splits a given text into chunks of a maximum length.

    Args:
        text (str): The text to be split.
        max_length (int): The maximum length of each chunk (default is 5000 characters).

    Returns:
        list: A list of text chunks, each of which has a length of no more than max_length characters.
    """
    chunks = []
    
    # Continue splitting the text until the remaining part is smaller than the max_length
    while len(text) > max_length:
        chunk = text[:max_length]  # Take a substring of the text up to max_length characters
        last_space = chunk.rfind(' ')  # Find the last space to avoid splitting in the middle of a word
        if last_space != -1:
            chunk = text[:last_space]  # If space is found, split at the space
            text = text[last_space + 1:]  # Update the remaining text after the space
        else:
            text = text[max_length:]  # If no space is found, split exactly at max_length
        chunks.append(chunk)  # Append the chunk to the list
    chunks.append(text)  # Add the last remaining part of the text
    return chunks


async def translate_news(news):
    """
    Translates the short description and main text of a single news article.

    Args:
        news (dict): A dictionary containing the news data with keys like 'news_short_text' and 'news_main_text'.

    Returns:
        dict: The same news dictionary but with additional keys:
              'news_short_text_translated' and 'news_main_text_translated' containing the translated versions.
    """

    # Translate the short description of the news
    translated_short_text = await translate_text(news["news_short_text"])

    # Translate the main text of the news
    translated_main_text = await translate_text(news["news_main_text"])

    # Add the translated texts to the original news dictionary
    news["news_short_text_translated"] = translated_short_text
    news["news_main_text_translated"] = translated_main_text
    return news


async def translate_all_news(news_list):
    """
    Translates all the news articles in the provided list asynchronously.

    Args:
        news_list (list): A list of dictionaries, where each dictionary contains the data of a single news article.

    Returns:
        list: A list of dictionaries with translated content.
    
    Each news article is translated concurrently using asyncio to speed up the process.
    """

    # Create a list of tasks to translate each news article concurrently
    tasks = [translate_news(news) for news in news_list]
    return await asyncio.gather(*tasks)
