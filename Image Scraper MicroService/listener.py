# -------------------------------------------------------------------
# Packages needed:
#   requests
#   beautifulsoup4

# Package install in terminal window:
#   pip install 'PackageName'
#   note: single quotes aren't required
# -------------------------------------------------------------------
# Original application for tv show watchlist tracker.
#   pre-programmed to bias results from rotten tomatoes and to ShowsImages
#   directory

# Can modify results to new application updating global variable:
#   QUERY_RELEVANCE
#   note: designed to handle full string input with spaces

# Can modify destination directory global variable:
#   DEST_DIR
#   note: destination directory defined as local to program directory;
#           potential future implementation to easily update and read
#           with 'os' module
# -------------------------------------------------------------------

import time
import os                   # might need for file creation or working on diff OS types
import requests
from bs4 import BeautifulSoup


# class FormatError(Exception):
#     """
#     Exception class when communication pipe isn't meeting format requirements.
#
#     :param Exception: defines to user-defined exception class
#     :return: None
#     """
#     print("Communication not meeting format 'type:value'")

# Global declarations
# relevance to add to query results
QUERY_RELEVANCE = 'rotten tomatoes'
# destination directory to save images
DEST_DIR = 'ShowsImages'


def main() -> None:
    """
    Continuous runs checking a communication pipe for a requested image. When
    prompted in image-service.txt:
        -reads the show title
        -searches for representative image on internet
        -downloads image to local directory
        -writes path to image to image-service.txt
    :return: n/a
    """

    while True:
        # Open image-service.txt
        with open('image-service.txt', 'r') as is_file:
            read_file = is_file.readline()
        is_file.close()

        if not read_file:
            continue

        # exception misbehavin now
        # if ':' not in read_file:
        #     raise FormatError

        # split read comm. into type and value
        split_read = read_file.split(":", 1)
        title_check = split_read[0]
        read_title = split_read[1]

        # check if communication contains a title or different type
        if title_check != 'title':
            time.sleep(5.0)
            continue
        else:
            # parse show title to google search query format; i.e. spaces
            # replaced with '+'
            query_title = read_title.replace(' ', '+')
            scrape_image(query_title)
            # might remove prepended local dir
            # with open('image-service.txt', 'w') as out_file:
            #     out_file.write("path:"f"./{DEST_DIR}/{query_title}.jpg")
            # out_file.close()


def scrape_image(query_title: str):
    """
    When called, searches provided show_title query on internet, downloads
    image to directory, and returns image path.
    :param: show_title(str): title of show to find representative image of.
    :return: n/a
    """
    # parse global relevance variable to google query format and page sourcing format
    if ' ' in QUERY_RELEVANCE:
        relevance_parsed = QUERY_RELEVANCE.replace(' ', '+')
        sourcing_parsed = QUERY_RELEVANCE.replace(' ', '')
    else:
        relevance_parsed, sourcing_parsed = QUERY_RELEVANCE

    # create search request url for show title with rotten tomatoes appended to ensure relevance
    # of google image results to application
    # text after '&' after google search query direct query to google images
    google_URL = f"https://www.google.com/search?q={relevance_parsed}+{query_title}"

    # take HTML page content
    google_HTML = requests.get(google_URL)
    google_content = BeautifulSoup(google_HTML.content, 'html.parser')

    # find all 'a' tags which include page links
    google_links = google_content.find_all('a')

    # find all relevant page links in a tag elements and append to a list
    sourcing_URLs = list()
    for URL in google_links:
        if f'{sourcing_parsed}' in URL['href']:
            st_idx = 7
            end_idx = URL['href'].find('&')
            sourcing_URLs.append(URL['href'][st_idx:end_idx])

    # take most relevant link
    source_URL = sourcing_URLs[0]

    # take HTML page content
    source_HTML = requests.get(source_URL)
    source_content = BeautifulSoup(source_HTML.content, 'html.parser')

    # find source img class tags
    image_tags = source_content.find_all()
    print(image_tags)
    img_links = list()
    for tag in image_tags:
        img_links.append(tag['src'])
    print('links: ', img_links)


if __name__ == "__main__":
    main()

