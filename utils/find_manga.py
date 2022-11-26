"""Functions that handle searching websites for the latest MHA chapter"""
import requests
import nums_from_string
from functools import reduce
from bs4 import BeautifulSoup
from utils.types import Result, Soup, Number
from typing import Tuple, Iterable

def find_latest_chapter(sources: Iterable) -> Tuple[Number, Result]:
    """
    Checks two sources for the latest MHA manga panels and 
    returns the results that have the latest chapter or simply
    the results from https://w1.heroacademiamanga.com/.
    """
    chapters_found = map(lambda url: find_latest_from_source(url), sources)
    latest_chapter = reduce(find_latest, chapters_found)
    return latest_chapter


def find_latest_from_source(url: str) -> Tuple[Number, Result]:
    """
    Returns the latest chapter available from the given source.

    :param url: The url of the given source
    """
    soup = get_soup(url)
    chapters = filter(lambda link: 'Chapter' in link.text, soup.find_all('a'))
    chapters = map(lambda link: (convert_to_number(link.text), link['href']), chapters)
    latest_chapter = reduce(find_latest, chapters)
    # For https://w32.readheroacademia.com/ only:
    # Check if the chapter is really there or if it's still counting down
    # Presence of an `iframe` indicates that the countdown timer is still
    # up, generally meaning that the panels are not available yet.
    if url == 'https://w32.readheroacademia.com/':
        chapter_present = len(get_soup(latest_chapter[1]).find_all('iframe')) == 0
        latest_chapter = latest_chapter if chapter_present else (latest_chapter[0]-1, None)
    
    return latest_chapter


def find_latest(prev: Tuple[Number, str], next: Tuple[Number, str]) -> Tuple[Number, Result]:
    """
    Returns the latest issue between the previous and the next.

    :param prev: The previous issue
    :param next: The next issue
    """
    return prev if prev[0] >= next[0] else next


def get_soup(url: str, parser: str = 'html5lib') -> Soup:
    """
    Returns soup for the requested issue

    :param url:    The url to request HTML from for soup
    :param parser: The parser to use for collecting soup. Default is html5lib 
    """
    html = requests.get(url)
    return BeautifulSoup(html.text, parser)


def convert_to_number(nstring: str) -> Number:
    """
    Extracts and returns the chapter/issue number from
    the given string.

    :param nstring: The string to extract digits from
    """
    return nums_from_string.get_nums(nstring)[0]
