"""
Custom type annotation definitions
"""
from bs4 import BeautifulSoup
from typing import TypeVar, Any, Union

Status = TypeVar('Status', bound=bool)
Result = TypeVar('Result', Any, None)
Soup = TypeVar('Soup', bound=BeautifulSoup)
Number = Union[float, int]