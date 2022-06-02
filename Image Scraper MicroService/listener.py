# -------------------------------------------------------------------
# Packages needed:
#   time
#   requests
#   urllib.request
#   beautifulsoup4
#   os

# Package install in terminal window:
#   pip install 'PackageName'
#   note: single quotes aren't required
# -------------------------------------------------------------------
# Original application for tv show watchlist tracker.
#   pre-programmed to bias results from Rotten Tomatoes and to ShowsImages
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
import requests
import urllib.request
import os
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
# communication pipe
COMM_PIPE = 'image-service.txt'
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
    validate_comm_pipe()
    validate_dest_dir()

    while True:
        read_contents = read_pipe()
        if not read_contents:
            continue

        # exception misbehavin now
        # if ':' not in read_file:
        #     raise FormatError

        title_check, read_title = split_contents(read_contents)

        # check if communication contains a title or different type
        if title_check != 'query':
            time.sleep(5.0)
            print('waiting')
            continue
        else:
            query_title = parse_title(read_title)
            img_source = scrape_image(query_title)

            download_to_dir(img_source, query_title)

            write_path(query_title)
            print('Success')
            continue


def scrape_image(query_title: str) -> str:
    """
    When called, searches provided show_title query on internet, downloads
    image to directory, and returns image path.
    :param: show_title(str): title of show to find representative image of.
    :return: parsed_source(str): html source for image
    """
    relevance_parsed, sourcing_parsed = parse_relevance()

    google_URL = create_google_url(relevance_parsed, query_title)

    google_content = get_google_content(google_URL)

    google_links = get_content_links(google_content)

    sourcing_URLs = parse_links(google_links, sourcing_parsed)

    source_content = get_source_content(sourcing_URLs[0])

    # find source images of desired class
    # if you're adapting to another application, inspect your source page's
    # classes and update
    source_class = 'PhotosCarousel__image'
    unparsed_source_links = list()
    page_images = source_content.find_all('img')
    for tag in page_images:
        if 'class' in tag.attrs and tag['class'] == [source_class]:
            unparsed_source_links.append(tag['src'])

    # check if source link has a resizing page prepended to source
    # if you're adapating to another application, inspect your source's
    # resizing delimiter
    parsed_source = None
    if 'resiz' in unparsed_source_links[0]:
        st_idx = unparsed_source_links[0].find('v2/') + 3
        parsed_source = unparsed_source_links[0][st_idx:]
    else:
        parsed_source = unparsed_source_links[0]

    return parsed_source


def validate_comm_pipe() -> None:
    """
    Checks if COMM_PIPE exists in local directory. If it doesn't, file is created.

    :return:
    """
    if not os.path.isfile(f"./{COMM_PIPE}"):
        with open(f"./{COMM_PIPE}") as cf:
            pass
        cf.close()


def validate_dest_dir() -> None:
    """
    Checks if DEST_DIR exists in local directory. If it doesn't, directory is created.

    :return: None
    """
    if not os.path.isdir(f"./{DEST_DIR}"):
        os.mkdir(f"./{DEST_DIR}")


def read_pipe() -> str:
    """
    Opens COMM_PIPE and reads current contents.

    :return: (str) current string contents of file.
    """
    with open(f"./{COMM_PIPE}", 'r') as is_file:
        read_file = is_file.readline()
    is_file.close()
    return read_file


def split_contents(read_contents: str) -> tuple:
    """
    Takes read contents from pipe and splits into two parts for parsing.

    :return: (tuple) tuple of strings for split read contents.
    """
    split_read = read_contents.split(":", 1)
    return split_read[0], split_read[1]


def parse_title(read_title: str) -> str:
    """
    Takes entered title information and parses contents to google search formatting.

    :param read_title: (str) entered title information.
    :return: (str) title parsed to google search formatting.
    """
    query_title = read_title.replace(' ', '+')
    return query_title


def download_to_dir(img_source, query_title) -> None:
    """
    Takes image source url and query title, downloads image to defined directory, and names
    image file as specified.

    :return: None
    """
    urllib.request.urlretrieve(img_source, f'./{DEST_DIR}/{query_title}.jpg')


def write_path(query_title: str) -> None:
    """
    Takes query title information and write downloaded image path to COMM_PIPE.

    :param query_title: (str) title parsed to google search formatting.
    :return: None
    """
    with open(f"./{COMM_PIPE}", 'w') as out_file:
        out_file.write("path:"f"./{DEST_DIR}/{query_title}.jpg")
    out_file.close()


def parse_relevance() -> tuple:
    """
    Parse global relevance variable to google query format and page sourcing format.

    :return: (tuple) parsed str values for relevance and sourcing.
    """
    if ' ' in QUERY_RELEVANCE:
        relevance_parsed = QUERY_RELEVANCE.replace(' ', '+')
        sourcing_parsed = QUERY_RELEVANCE.replace(' ', '')
    else:
        relevance_parsed, sourcing_parsed = QUERY_RELEVANCE
    return relevance_parsed, sourcing_parsed


def create_google_url(relevance_parsed: str, query_title: str) -> str:
    """
    Takes parsed relevance and query title variables and creates a google search query URL.

    :return: (str) google search query URL.
    """
    # create search request url for show title with rotten tomatoes appended to ensure relevance
    # of google image results to application
    # text after '&' after google search query direct query to google images
    google_URL = f"https://www.google.com/search?q={relevance_parsed}+{query_title}"
    return google_URL


def get_google_content(google_URL: str) -> str:
    """
    Take google_URL, parse HTML content, and return content from the page.

    :param google_URL: (str) google search query URL.
    :return: (str) parsed content of html google search query.
    """
    google_HTML = requests.get(google_URL)
    google_content = BeautifulSoup(google_HTML.content, 'html.parser')
    return google_content


def get_content_links(google_content: str) -> str:
    """

    :param google_content: (str) parsed content of html google search query.
    :return:
    """
    # find all 'a' tags which include page links
    google_links = google_content.find_all('a')
    return google_links


def parse_links(google_links: str, sourcing_parsed: str) -> list:
    """
    Parse links on google search query and add each to a list.

    :param google_links: (str) links from google search page content.
    :param sourcing_parsed: (str) sourcing relevance variable parsed.
    :return: (list) list of links from google search query page.
    """
    sourcing_URLs = list()
    for URL in google_links:
        if f'{sourcing_parsed}' in URL['href']:
            st_idx = 7
            end_idx = URL['href'].find('&')
            sourcing_URLs.append(URL['href'][st_idx:end_idx])
    return sourcing_URLs


def get_source_content(source_URL: str) -> str:
    """
    Take source_URL, parse HTML content, and return content from the page.

    :param source_URL: (str) source query URL.
    :return: (str) parsed content of html source query.
    """
    source_HTML = requests.get(source_URL)
    source_content = BeautifulSoup(source_HTML.content, 'html.parser')
    return source_content

if __name__ == "__main__":
    main()
