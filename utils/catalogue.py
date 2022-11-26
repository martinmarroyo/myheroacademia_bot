"""
Functions that manage the MHA-catalogue.json file
"""
import json
from pathlib import Path
from utils.types import Status, Result 
from typing import Mapping, Tuple, Iterable

def create_catalogue_entry(prev_entry: Mapping, day: str) -> Mapping:
    """
    Creates a new catalogue entry based on the previous entry.
    
    :param prev_entry: The previous catalogue entry
    :param day: The date to add in `yyyy-mm-dd` format
    """
    return {
        'date':         day,
        'latest_issue': prev_entry['next_issue'],
        'next_issue':   prev_entry['next_issue'] + 1,
        'notified':     False
    }
    
    
def check_catalogue(catalogue: Iterable[Mapping], path: Path, day: str) -> Tuple[Status, Result]:
    """
    Checks the catalogue to see if we already have the latest issue. If we do, then a new
    catalogue entry is created to help find the next one. If not, we continue to check for
    the next issue until it is found.
    
    :param catalogue: The catalogue of MHA issues that we currently have
    :param path: Path to the mha-catalogue.json file 
    :param day: The date to check against in `yyyy-MM-dd` format
    """
    latest = catalogue[-1]
    status, result = False, latest
    if latest['notified']:
        result = create_catalogue_entry(latest, day)
        catalogue.append(result)
        updated, err = update_catalogue(path, catalogue)
        if err: raise err
        status = updated
    elif not latest['notified'] and latest['date'] != day:
        # Update the latest date until we find the next issue
        catalogue[-1]['date'] = day
        updated, err = update_catalogue(path, catalogue)
        if err: raise err
        status, result = updated, catalogue[-1]
    
    return (status, result)


def get_catalogue(path: Path) -> Iterable[Mapping]:
    """
    Opens the mha-catalogue.json file and
    returns a json object for parsing
    
    :param path: Path to the mha-catalogue.json file
    """
    with open(path, 'r') as file:
        catalogue = json.loads(file.read())
    
    return catalogue


def update_catalogue(path: Path, updates: Iterable[Mapping]) -> Tuple[Status, Result]:
    """
    Writes changes to the mha-catalogue.json file back to the source.
    
    :param path: Path to mha-catalogue.json file
    :param updates: Updated catalogue to write
    """
    status, result = False, None
    try:
        with open(path, 'w') as file:
            json.dump(updates, file)
        
        status = True
    except Exception as ex:
        result = ex
    finally:
        return (status, result)