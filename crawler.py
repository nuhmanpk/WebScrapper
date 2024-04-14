# /usr/bin/nuhmanpk/bughunter0 

import asyncio
import logging
from scraper import scrape
import os
from urllib.parse import urljoin, urlparse, unquote
from dotenv import load_dotenv
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

CRAWL_LOG_CHANNEL = os.getenv('CRAWL_LOG_CHANNEL')

def get_safe_filename(url):
    parsed_url = urlparse(url)
    return unquote(parsed_url.netloc + parsed_url.path).replace('/', '_').replace(':', '_')

async def crawl(bot, url):
    try:
        _, soup = await scrape(url)
        filename = get_safe_filename(url)
        file_path = f"{filename}.txt"
        with open(file_path, "a+") as file_write:
            for para in soup.find_all("p"):
                paragraph = para.get_text()
                file_write.write(f"{paragraph}\n\n")
        await bot.send_document(document=file_path,chat_id=CRAWL_LOG_CHANNEL,caption='@BughunterBots')
        await asyncio.sleep(5)
        os.remove(file_path)
        logger.info(f"Crawled and saved content from {url}")
    except Exception as e:
        await asyncio.sleep(1)
        os.remove(file_path)
        logger.error(f"Error crawling {url}: {e}")

async def crawl_web(bot,query):
    try:
        message = query.message
        base_url = message.text
        _, soup = await scrape(base_url)
        visited_urls = set()
        links = soup.find_all('a', href=True)
        txt = await message.reply('Crawling ...') 
        for link in links:
            next_url = urljoin(base_url, link['href'])
            if next_url not in visited_urls:
                await txt.edit(f'Crawling {next_url}')
                await crawl(bot, next_url)
                await asyncio.sleep(2)
                visited_urls.add(next_url)
        await txt.edit(f'Completed')
    except Exception as e:
        logger.error(f"Error crawling {base_url}: {e}")
        raise e
