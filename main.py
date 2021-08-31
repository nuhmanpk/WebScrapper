# © BugHunterCodeLabs ™
# © bughunter0
# 2021
# Copyright - https://en.m.wikipedia.org/wiki/Fair_use

import os 
from os import error
import pyrogram
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types import User, Message
from bs4 import BeautifulSoup
import html5lib
import requests 
    
bughunter0 = Client(
    "WebScrapperBot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)

@bughunter0.on_message(filters.command(["start"]))
async def start(bot, message):
   await message.reply_text("Join @BugHunterBots")


@bughunter0.on_message((filters.regex("https") | filters.regex("http") | filters.regex("www")) & (filters.forwarded | filters.reply | filters.private))
async def scrapping(bot,message):
 try:
    txt = await message.reply_text("Validating Link")
    url=str(message.text)
    request = requests.get(url)
    await txt.edit(text=f"Getting Raw Data from {url}",disable_web_page_preview=True)
    with open(f'RawData-{message.chat.username}.txt', 'a+') as text_path:  
         file_write = open(f'RawData-{message.chat.username}.txt','a+')
         file_write.write(f"{request.content}")
         await message.reply_document(f"RawData-{message.chat.username}.txt",caption="©@BugHunterBots")
         os.remove(f"RawData-{message.chat.username}.txt")
    await txt.delete()
 except Exception as error:
          print (error)
          await message.reply_text(text=f"{error}",disable_web_page_preview=True)            
          await txt.delete()
          return
 try:
    txt = await message.reply_text(text=f"Getting HTML code from {url}",disable_web_page_preview=True)
    soup = BeautifulSoup(request.content, 'html5lib') 
    with open(f'HtmlData-{message.chat.username}.txt', 'a+') as text_path:
          file_write = open(f'HtmlData-{message.chat.username}.txt','a+')
          soup.data=soup.prettify()
          file_write.write(f"{soup.data}")
          await message.reply_document(f"HtmlData-{message.chat.username}.txt",caption="©@BugHunterBots")
          os.remove(f"HtmlData-{message.chat.username}.txt")
    await txt.delete()
 except Exception as error:
          await message.reply_text(text=f"{error}",disable_web_page_preview=True)            
          await txt.delete()
          return
 try:
    txt = await message.reply_text(f"Getting all Links from {url}",disable_web_page_preview=True)
    with open(f'AllLinks-{message.chat.username}.txt', 'a+') as text_path:
          file_write = open(f'AllLinks-{message.chat.username}.txt','a+')
          for link in soup.find_all('a'):
              links=link.get('href')
              file_write.write(f"{links}\n\n")
          await message.reply_document(f"AllLinks-{message.chat.username}.txt",caption="©@BugHunterBots")
          os.remove(f"AllLinks-{message.chat.username}.txt")
    await txt.delete()
 except Exception as error:
          await message.reply_text(text="No Links Found !!",disable_web_page_preview=True)            
          await txt.delete()
          
 try:
    txt = await message.reply_text(f"Getting all Paragraph from {url}",disable_web_page_preview=True)
    with open(f'AllParagraph-{message.chat.username}.txt', 'a+') as text_path:
          file_write = open(f'AllParagraph-{message.chat.username}.txt','a+')
          paragraph=''
          for para in soup.find_all('p'):
              paragraph=para.get_text()
              file_write.write(f"{paragraph}\n\n")
          await txt.delete()
          await message.reply_document(f"AllParagraph-{message.chat.username}.txt",caption="©@BugHunterBots")
          os.remove(f"AllParagraph-{message.chat.username}.txt")
          
          
 except Exception as error:
          await message.reply_text(text="No Paragraphs Found !!",disable_web_page_preview=True)            
          await txt.delete()
          return

bughunter0.run()
