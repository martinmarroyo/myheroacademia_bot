"""
Custom type annotation definitions
"""
from bs4 import BeautifulSoup
from typing import  TypeVar, Any

Status = TypeVar('Status', bound=bool)
Result = TypeVar('Result', Any, None)
Soup = TypeVar('Soup', bound=BeautifulSoup)