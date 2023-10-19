# © BugHunterCodeLabs ™
# © bughunter0
# © Nuhman Pk
# 2021 - 2023
# Copyright - https://en.m.wikipedia.org/wiki/Fair_use

import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from bs4 import BeautifulSoup
import requests
import shutil
from urllib.parse import quote


# app = Client(
#     "WebScrapperBot",
#     bot_token=os.environ["BOT_TOKEN"],
#     api_id=int(os.environ["API_ID"]),
#     api_hash=os.environ["API_HASH"]
# )

app = Client(
    "WebScrapperBot",
    bot_token='TOKEN_HERE',
    api_id=int('ID_AS_STRING'),
    api_hash='HASH_HERE'
)


REPO = 'https://github.com/nuhmanpk/WebScrapper/'

FINISHED_PROGRESS_STR = "▓"
UN_FINISHED_PROGRESS_STR = "░"

START_BUTTON = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Raw Data', callback_data='cbrdata'),
            InlineKeyboardButton('HTML Data', callback_data='cbhtmldata')
        ],
        [
            InlineKeyboardButton('All Links', callback_data='cballlinks'),
            InlineKeyboardButton(
                'All Paragraphs', callback_data='cballparagraphs')
        ],
        [
            InlineKeyboardButton('All Images', callback_data='cballimages')
        ]
    ]
)
CLOSE_BUTTON = InlineKeyboardMarkup(
    [[InlineKeyboardButton('Back', callback_data='cbclose')]]
)


@app.on_message(filters.command(["start"]))
async def start(_, message: Message):
    # Edit Your Start string here
    text = f"Hello , I am a web scrapper bot." \
        "\nSend me any link for scrapping.\n\nJoin @BugHunterBots"
    await message.reply_text(text=text, disable_web_page_preview=True, quote=True)


async def download_image(base_url, image_url, idx):
    try:
        r = requests.get(image_url, stream=True)
        r.raise_for_status()
        with open(f"image{idx}.jpg", 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
        with open(f"image{idx}.jpg", "rb") as f:
            image_data = f.read()
        os.remove(f"image{idx}.jpg")
        return image_data
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Request Exception: {err}")
    except Exception as e:
        print(f"Error downloading image from {image_url}: {e}")
    return None


@app.on_callback_query()
async def cb_data(bot, update):
    if update.data == "cbrdata":
        await raw_data_scraping(update)
    elif update.data == "cbhtmldata":
        await html_data_scraping(update)
    elif update.data == "cballlinks":
        await all_links_scraping(update)
    elif update.data == "cballparagraphs":
        await all_paragraph_scraping(update)
    elif update.data == "cballimages":
        await all_images_scraping(update)
    else:
        await update.message.edit_text(
            text="something",
            disable_web_page_preview=True,
            reply_markup=START_BUTTON
        )


async def scrape(url):
    try:
        request = requests.get(url)
        soup = BeautifulSoup(request.content, 'html5lib')
        return request, soup
    except Exception as e:
        print(e)
        return None, None


async def raw_data_scraping(query):
    try:
        message = query.message
        request, soup = await scrape(message.text)
        file_write = open(f'RawData-{message.chat.username}.txt', 'a+')
        file_write.write(f"{request.content}")
        file_write.close()
        await message.reply_document(f"RawData-{message.chat.username}.txt", caption="©@BugHunterBots", quote=True)
        os.remove(f"RawData-{message.chat.username}.txt")
        return
    except Exception as e:
        os.remove(f"RawData-{message.chat.username}.txt")
        error = f"ERROR: {(str(e))}"
        error_link = f"{REPO}/issues/new?title={quote(error)}"
        text = f'Something Bad occurred !!!\nCreate an issue here'
        issue_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Create Issue", url=error_link)]])
        await message.reply_text(text, disable_web_page_preview=True, quote=True, reply_markup=issue_markup)
        return e


async def html_data_scraping(query):
    try:
        message = query.message
        request, soup = await scrape(message.text)
        file_write = open(f'HtmlData-{message.chat.username}.txt', 'a+')
        soup.data = soup.prettify()
        file_write.write(f"{soup.data}")
        file_write.close()
        await message.reply_document(f"HtmlData-{message.chat.username}.txt", caption="©@BugHunterBots", quote=True)
        os.remove(f"HtmlData-{message.chat.username}.txt")
    except Exception as e:
        os.remove(f"HtmlData-{message.chat.username}.txt")
        error = f"ERROR: {(str(e))}"
        error_link = f"{REPO}/issues/new?title={quote(error)}"
        text = f'Something Bad occurred !!!\nCreate an issue here'
        issue_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Create Issue", url=error_link)]])
        await message.reply_text(text, disable_web_page_preview=True, quote=True, reply_markup=issue_markup)
        return e


async def all_links_scraping(query):
    try:
        message = query.message
        request, soup = await scrape(message.text)
        file_write = open(f'AllLinks-{message.chat.username}.txt', 'a+')
        for link in soup.find_all('a'):
            links = link.get('href')
            file_write.write(f"{links}\n\n")
        file_write.close()
        await message.reply_document(
            f"AllLinks-{message.chat.username}.txt",
            caption="©@BugHunterBots"
        )
        os.remove(f"AllLinks-{message.chat.username}.txt")
    except Exception as e:
        os.remove(f"AllLinks-{message.chat.username}.txt")
        error = f"ERROR: {(str(e))}"
        error_link = f"{REPO}/issues/new?title={quote(error)}"
        text = f'Something Bad occurred !!!\nCreate an issue here'
        issue_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Create Issue", url=error_link)]])
        await message.reply_text(text, disable_web_page_preview=True, quote=True, reply_markup=issue_markup)
        return e


async def all_paragraph_scraping(query):
    try:
        message = query.message
        request, soup = await scrape(message.text)
        file_write = open(f'AllParagraph-{message.chat.username}.txt', 'a+')
        paragraph = ""
        for para in soup.find_all('p'):
            paragraph = para.get_text()
            file_write.write(f"{paragraph}\n\n")
        file_write.close()

        await message.reply_document(
            f"AllParagraph-{message.chat.username}.txt",
            caption="©@BugHunterBots",
            quote=True
        )
        os.remove(f"AllParagraph-{message.chat.username}.txt")
    except Exception as e:
        os.remove(f"AllParagraph-{message.chat.username}.txt")
        error = f"ERROR: {(str(e))}"
        error_link = f"{REPO}/issues/new?title={quote(error)}"
        text = f'Something Bad occurred !!!\nCreate an issue here'
        issue_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Create Issue", url=error_link)]])
        await message.reply_text(text, disable_web_page_preview=True, quote=True, reply_markup=issue_markup)
        return e


async def all_images_scraping(query):
    try:
        message = query.message
        txt = await message.reply_text("Scraping url ...", quote=True)
        request, soup = await scrape(message.text)
        image_links = []
        for img_tag in soup.find_all('img'):
            img_url = img_tag.get('src')
            image_links.append(img_url)

        await txt.edit(text=f"Found {len(image_links)} Images", disable_web_page_preview=True)

        if len(image_links):
            status = await message.reply_text("Downloading...", quote=True)
            folder_name = f"{message.chat.id}"
            os.makedirs(folder_name, exist_ok=True)
            for idx, image_link in enumerate(image_links):
                image_data = await download_image(message.text, image_link, idx)
                if image_data:
                    with open(f"{folder_name}/image{idx}.jpg", "wb") as file:
                        file.write(image_data)
                    progress, finished_length = await progress_bar(idx+1, len(image_links))
                    try:
                        await status.edit(f"Percentage: {finished_length*10}%\nProgress: {progress}\n")
                    except:
                        pass
            zip_filename = f"{message.chat.id}.zip"
            shutil.make_archive(folder_name, 'zip', folder_name)

            await message.reply_document(open(zip_filename, "rb"), caption="Here are the images!")
            await status.delete()
            shutil.rmtree(folder_name)
            os.remove(zip_filename)
            return
        else:
            await txt.edit(text=f"No Images Found!!!", disable_web_page_preview=True)
            return
    except Exception as e:
        error = f"ERROR: {(str(e))}"
        error_link = f"{REPO}/issues/new?title={quote(error)}"
        text = f'Something Bad occurred !!!\nCreate an issue here'
        issue_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Create Issue", url=error_link)]])
        await message.reply_text(text, disable_web_page_preview=True, quote=True, reply_markup=issue_markup)
        return e


async def progress_bar(current, total):
    percentage = current / total
    finished_length = int(percentage * 10)
    unfinished_length = 10 - finished_length
    progress = f"{FINISHED_PROGRESS_STR * finished_length}{UN_FINISHED_PROGRESS_STR * unfinished_length}"
    return progress, finished_length


@app.on_message((filters.regex("https") | filters.regex("http") | filters.regex("www")) & filters.private)
async def scrapping(bot, message):
    await send_message_with_options(message)


async def send_message_with_options(message):
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('Raw Data', callback_data='cbrdata',),
                InlineKeyboardButton('HTML Data', callback_data='cbhtmldata')
            ],
            [
                InlineKeyboardButton('All Links', callback_data='cballlinks'),
                InlineKeyboardButton(
                    'All Paragraphs', callback_data='cballparagraphs')
            ],
            [
                InlineKeyboardButton('All Images', callback_data='cballimages')
            ]
        ]
    )
    await message.reply_text('Choose an Option')
    await message.reply_text(message.text, reply_markup=reply_markup)


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

app.run(print('Bot Running....'))
