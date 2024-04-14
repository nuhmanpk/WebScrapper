# © BugHunterCodeLabs ™
# © bughunter0
# © Nuhman Pk
# 2021 - 2024
# Copyright - https://en.m.wikipedia.org/wiki/Fair_use

# /usr/bin/nuhmanpk/bughunter0 

import os
from pyrogram import Client, filters
from dotenv import load_dotenv
import os
from pyrogram.types import Message
from scraper import (
    all_audio_scraping,
    all_images_scraping,
    all_links_scraping,
    all_paragraph_scraping,
    all_pdf_scraping,
    all_video_scraping,
    extract_cookies,
    extract_local_storage,
    html_data_scraping,
    raw_data_scraping,
    extract_metadata,
    capture_screenshot,
    record_screen
)
from crawler import crawl_web
from utils import OPTIONS, START_BUTTON, START_TEXT

load_dotenv()

bot_token = os.getenv("BOT_TOKEN")
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")

CRAWL_LOG_CHANNEL = os.getenv('CRAWL_LOG_CHANNEL')

if bot_token is None or api_id is None or api_hash is None:
    raise ValueError(
        "Please set the BOT_TOKEN, API_ID, and API_HASH environment variables."
    )

app = Client(
    "WebScrapperBot", bot_token=bot_token, api_id=int(api_id), api_hash=api_hash
)


@app.on_message(filters.command(["start"]))
async def start(_, message: Message):
    # Edit Your Start string here
    text = START_TEXT
    await message.reply_text(text=text, disable_web_page_preview=True, quote=True)


@app.on_callback_query()
async def cb_data(bot:Client, update):
    if update.data == "cbrdata":
        await raw_data_scraping(update)
    elif update.data == "cbhtmldata":
        await html_data_scraping(update)
    elif update.data == "cballlinks":
        await all_links_scraping(update)
    elif update.data == "cballparagraphs":
        await all_paragraph_scraping(update)
    elif update.data == "cballimages":
        await all_images_scraping(bot,update)
    elif update.data == "cballaudio":
        await all_audio_scraping(bot,update)
    elif update.data == "cballvideo":
        await all_video_scraping(bot,update)
    elif update.data == "cballpdf":
        await all_pdf_scraping(update)
    elif update.data == "cbmetadata":
        await extract_metadata(update)
    elif update.data == "cbcookies":
        await extract_cookies(update)
    elif update.data == "cblocalstorage":
        await extract_local_storage(update)
    elif update.data == "cbscreenshot":
        await capture_screenshot(update)
    elif update.data == "cbscreenrecord":
        await record_screen(update)
    elif update.data == "cdstoptrasmission":
        bot.stop_transmission()
    elif update.data == 'cbcrawl':
        if CRAWL_LOG_CHANNEL:
            await crawl_web(bot,update)
        else:
            await update.message.reply('You must provide a Log Channel ID')

    else:
        await update.message.edit_text(
            text=START_TEXT, disable_web_page_preview=True, reply_markup=START_BUTTON
        )


@app.on_message(
    (filters.regex("https") | filters.regex("http") | filters.regex("www"))
    & filters.private
)
async def scrapping(bot, message):
    await send_message_with_options(message)


async def send_message_with_options(message):
    reply_markup = OPTIONS
    await message.reply_text("Choose an Option")
    await message.reply_text(
        message.text, reply_markup=reply_markup, disable_web_page_preview=True
    )


# Use soup.find_all('tag_name') to Extract Specific Tag Details
"""
soup.title
# <title>This is Title</title>

soup.title.name
# u'title'

soup.title.string
# u'This is a string'

soup.title.parent.name
# u'head'
"""

app.run(print("Bot Running...."))
