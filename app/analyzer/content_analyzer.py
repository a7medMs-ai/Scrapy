from bs4 import BeautifulSoup
import re

def extract_page_data(html_content: str, page_url: str, page_name: str, counter: int) -> dict:
    '''
    Extracts structured data from an HTML page for localization analysis.

    Parameters:
    - html_content (str): Raw HTML content of the page.
    - page_url (str): The original URL of the page.
    - page_name (str): The name to be displayed in the report.
    - counter (int): Page counter for ordering in the report.

    Returns:
    - dict: A dictionary with analysis data for the page.
    '''

    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract text content (excluding script/style)
    for tag in soup(['script', 'style', 'noscript']):
        tag.decompose()
    visible_text = soup.get_text(separator=' ', strip=True)

    # Word count logic
    words = re.findall(r'\\b\\w+\\b', visible_text)
    word_count = len(words)

    # Segment count logic: split by sentence-ending punctuation
    segments = re.split(r'[.!?؟!]+', visible_text)
    segments = [s.strip() for s in segments if s.strip()]
    segment_count = len(segments)

    # Check for media (img/video/audio)
    has_media = bool(soup.find(['img', 'video', 'audio', 'iframe']))

    return {
        'Page Counter': counter,
        'Page Name': page_name,
        'Word Count': word_count,
        'Segments': segment_count,
        'Has Media': has_media,
        'Page URL': page_url,
        'Page Content': visible_text,
        'Localization Notes': ''  # Empty field for translators to add notes
    }
