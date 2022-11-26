"""Functions that handle searching websites for the latest MHA chapter"""
import requests
from bs4 import BeautifulSoup
from utils.types import Result, Soup
from typing import Tuple

def find_latest_chapter() -> Tuple[float, Result]:
    """
    Checks two sources for the latest MHA manga panels and 
    returns the results that have the latest chapter or simply
    the results from https://w1.heroacademiamanga.com/.
    """
    chapter_s1, s1_url = find_latest_heroacademiamanga()
    chapter_s2, s2_url = find_latest_readheroacademia()
    chapter, url = 0, None
    if chapter_s1 >= chapter_s2:
        chapter, url = chapter_s1, s1_url
    elif chapter_s2 >= chapter_s1:
        chapter, url = chapter_s2, s2_url
    return (chapter, url)
        

def find_latest_heroacademiamanga() -> Tuple[float, str]:
    """
    Finds current chapters listed at https://w1.heroacademiamanga.com/
    """
    soup = get_soup('https://w1.heroacademiamanga.com/')
    latest_chapter, url = [
        (link.text.split(' ')[1], link['href']) 
        for link in soup.find_all('a') 
        if link.text.startswith('Chapter ')
    ][0]
    if not latest_chapter.isalnum():
        latest_chapter = ''.join([num for num in latest_chapter if num.isdigit()])
    latest_chapter = float(latest_chapter)
    return (latest_chapter, url)


def find_latest_readheroacademia() -> Tuple[float, Result]:
    """
    Finds current chapters listed at https://w32.readheroacademia.com/
    """
    soup = get_soup('https://w32.readheroacademia.com/')
    latest_ch, url = [
        (link.text.strip(), link['href']) 
        for link in soup.find_all('a') 
        if 'Chapter' in link.text
    ][0]
    latest_ch = latest_ch.split(' ')[-1]
    if not latest_ch.isalnum():
        latest_ch = ''.join([num for num in latest_ch if num.isdigit()])
    latest_ch = float(latest_ch)
    # Check if the chapter is really there or if it's still counting down
    # Presence of an `iframe` indicates that the countdown timer is still
    # up, generally meaning that the panels are not available yet.
    chapter_present = len(get_soup(url).find_all('iframe')) == 0
    latest_ch = latest_ch if chapter_present else latest_ch - 1
    url = url if chapter_present else None
    return (latest_ch, url)


def get_soup(url: str) -> Soup:
    """
    Returns soup for the requested issue
    """
    html = requests.get(url)
    return BeautifulSoup(html.text, 'html5lib')