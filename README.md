# My Hero Academia Bot

![my_hero_academia](https://img1.hulu.com/user/v3/artwork/36e318dc-3daf-47fb-8219-9e3cb5cd28f2?base_image_bucket_name=image_manager&base_image=2d0d3308-9323-4716-b7d8-03f171c844af&size=1200x630&format=jpeg)

I love My Hero Academia. I'm an avid reader of the weekly manga that comes out. I read the early English translations of the scans that come out every Friday (mostly). The release times vary, but it's generally available in the afternoon or evening most Fridays. 

For practice (and novelty,) I decided to automate the process of finding the next issue. I wanted something that would check a couple of different sources for the early scans and then send me a link to the latest issue of the manga.

This bot checks a couple of known websites to see if the newest mangas scans are available. Once it finds the latest issue, it will send me a text message and an email with the link. The bot will also keep track of the current, previous, and upcoming issues.

## Tools used

The bot is written in Python. I primarily used `Docker`, `requests`, `BeautifulSoup`, and `twilio` to build it out. `requests` and `BeautifulSoup` are used to scrape the sites to find the latest chapter. Once the latest chapter is found, I use `twilio` to send me a text message with url. `Docker` is used to package the bot for deployment. 

## Program Flow

The chart below describes the general flow of execution:

![mhabot - flow of execution](assets\mhabot-flowchart.PNG)

## The `MHA-Catalogue` File

The bot uses the `mha-catalog.json` file to keep track of which chapter to look for, as well as the issues we have already found. It holds information about the date that previous issues were found, the issue number, the next issue number, and whether or not I had been notified about that issue. Here is the structure:
```
{
    'date': 'YYYY-MM-DD',
    'latest_issue': X,
    'next_issue': X+1,
    'notified': false
}
```
## The `env_file`

The `env_file` is used to supply credentials for `twilio`. These are the variables that the bot expects to find in the execution environment:
```
TWILIO_SID=<TWILIO SID>
TWILIO_AUTH_TOKEN=<TWILIO_AUTH_TOKEN>
MY_PHONE=<YOUR PHONE NUMBER>
TWILIO_NUMBER=<TWILIO_NUMBER>
```

## How to Run the bot

To run the bot, you can use `Docker` or run the Python files directly.

### With Docker

1. Ensure that you have `Docker` installed on your system
2. Move into the base directory of this project (`myheroacademia_bot`)
3. Build the `Docker` image
```bash
docker build -t mhabot:0.1 .
```
4. Run the bot
```bash
docker run --name mhabot --env-file env_file -d mhabot:0.1
```

### Without Docker

1. Move into the base directory of this project (`myheroacademia_bot`)
2. Create a virtual environment (optional, but recommended)
3. Install dependencies outlined in the `requirements.txt` file
```bash
pip install -r requirements.txt
```
4. Run the bot
```bash
python3 -m main
```