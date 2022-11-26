import os
import sys
from loguru import logger
from utils import catalogue as ctlg
from utils import find_manga as fm
from twilio.rest import Client
from pathlib import Path
from utils.types import Status, Result
from datetime import datetime, date
from typing import Tuple, Iterable, Mapping

def send_message(message: str) -> Tuple[Status, Result]:
    """
    Sends a text message to my phone using the Twilio API
    
    :param message: The message string to send via SMS
    """    
    client = Client(os.getenv('TWILIO_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
    status, result = False, None
    try:
        client.messages.create(
            to =    os.getenv('MY_PHONE'), 
            from_ = os.getenv('TWILIO_NUMBER'), 
            body =  message
        )
        status = True
    except Exception as ex:
        result = ex
    finally:
        return (status, result)


def mha_bot(day: str = None) -> Tuple[Status, Result]:
    """
    An automated process that checks for the next early
    release of the My Hero Academia manga each Friday
    """
    date_ = datetime.strftime(date.today(), '%Y-%m-%d') if day is None else day
    status = False
    # Check catalogue
    path = Path.cwd() /'utils'/'data'/'mha-catalogue.json'
    catalogue = ctlg.get_catalogue(path)
    has_latest, latest = ctlg.check_catalogue(catalogue, path, date_)
    # Break if we already have the latest issue
    if has_latest: return (status, latest)
    # Otherwise, check websites for latest chapter
    latest_chapter, url = fm.find_latest_chapter()
    if latest_chapter == latest['latest_issue']:
        # Found latest issue. Send message, update catalog, & return results
        message_status, err = notify_and_update(url, path, catalogue)
        if err: raise err
        return (message_status, latest)
    # If we get here, then the issue still isn't out
    return (False, 'Issue not present')


def notify_and_update(url: str, path: Path, catalogue: Iterable[Mapping]) -> Tuple[Status, Result]:
    """
    Sends a text message with the url to the latest chapter and updates
    the mha-catalogue.json file

    :param url: The url of the latest chapter
    :param path: The path to the mha-catalogue.json file
    :param catalogue: The contents of the mha-catalogue.json file
    """
    message = f'The next issue is here! \n{url}'
    status, result = send_message(message)
    if status:
        # Update catalogue only if message was sent successfully
        catalogue[-1]['notified'] = True
        ctlg.update_catalogue(path, catalogue)

    return status, result


if __name__ == '__main__':
    args = sys.argv[1:]
    day = args[0] if args else None
    status, _ = mha_bot(day=day)
    logger.info(f'Do we have the next issue? {"Yes" if status else "No"}')