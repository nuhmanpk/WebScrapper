import asyncio
import time
import requests
import os
import shutil
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bs4 import BeautifulSoup
from urllib.parse import quote
from utils import REPO
from helpers import download_image, download_media, download_pdf, progress_bar

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
        await asyncio.sleep(1)
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
        await asyncio.sleep(1)        
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
        await asyncio.sleep(1)
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
        await asyncio.sleep(1)        
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

        text = await txt.edit(text=f"Found {len(image_links)} Images", disable_web_page_preview=True)

        if len(image_links):
            status = await message.reply_text("Checking...", quote=True)
            folder_name = f"{message.chat.id}-images"
            os.makedirs(folder_name, exist_ok=True)
            for idx, image_link in enumerate(image_links):
                image_data = await download_image(message.text, image_link, idx)
                if image_data:
                    with open(f"{folder_name}/image{idx}.jpg", "wb") as file:
                        file.write(image_data)
                    progress, finished_length = await progress_bar(idx+1, len(image_links))
                    try:
                        await status.edit(f"Downloding...\nPercentage: {finished_length*10}%\nProgress: {progress}\n")
                    except:
                        pass
            await status.edit('Uploading ....')
            zip_filename = f"{message.chat.id}-images.zip"
            shutil.make_archive(folder_name, 'zip', folder_name)

            await message.reply_document(open(zip_filename, "rb"), caption="Here are the images! \n @BUghunterBots")
            await status.delete()
            await text.delete()
            shutil.rmtree(folder_name)
            await asyncio.sleep(1)
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
    
    
async def all_audio_scraping(query):
    try:
        message = query.message
        txt = await message.reply_text("Scraping url ...", quote=True)
        request, soup = await scrape(message.text)
        audio_links = [link['src'] for link in soup.find_all('audio')]
        if len(audio_links):
            await txt.edit(text=f"Found {len(audio_links)} Images", disable_web_page_preview=True)
            status = await message.reply_text("Checking...", quote=True)
            folder_name = f"{message.chat.id}-audios"
            os.makedirs(folder_name, exist_ok=True)
            for idx, audio_link in enumerate(audio_links):
                audio_data = await download_media(message.text, audio_link, idx, 'audio')
                if audio_data:
                    with open(f"{folder_name}/audio{idx}.jpg", "wb") as file:
                        file.write(audio_data)
                    progress, finished_length = await progress_bar(idx+1, len(audio_links))
                    try:
                        await status.edit(f"Downloding...\nPercentage: {finished_length*10}%\nProgress: {progress}\n")
                    except:
                        pass
                await status.edit(f'Downloaded {idx + 1}/{len(audio_links)}')
            await status.edit('Uploading ....')
            zip_filename = f"{message.chat.id}-audios.zip"
            shutil.make_archive(folder_name, 'zip', folder_name)

            await message.reply_document(open(zip_filename, "rb"), caption="Here are the images! \n @BUghunterBots")
            await status.delete()
            await txt.delete()
            shutil.rmtree(folder_name)
            await asyncio.sleep(1)
            os.remove(zip_filename)
            return
        else:
            await txt.edit(text=f"No Audios Found!!!", disable_web_page_preview=True)
            return
            
    except Exception as e:
        error = f"ERROR: {(str(e))}"
        error_link = f"{REPO}/issues/new?title={quote(error)}"
        text = f'Something Bad occurred !!!\nCreate an issue here'
        issue_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Create Issue", url=error_link)]])
        await message.reply_text(text, disable_web_page_preview=True, quote=True, reply_markup=issue_markup)
        print(e)
        return e


async def all_video_scraping(query):
    try:
        message = query.message
        txt = await message.reply_text("Scraping url ...", quote=True)
        request, soup = await scrape(message.text)
        
        video_tags = soup.find_all('video')

        video_links = [video['src'] if video.has_attr('src') else video.find('source')['src'] for video in video_tags]

        txt = await txt.edit(text=f"Found {len(video_links)} Videos", disable_web_page_preview=True)
        
        if len(video_links):
            status = await message.reply_text("Checking...", quote=True)
            folder_name = f"{message.chat.id}-videos"
            os.makedirs(folder_name, exist_ok=True)
            
            for idx, video_link in enumerate(video_links):
                progress, finished_length = await progress_bar(idx + 1, len(video_links))
                
                try:
                    await status.edit(f"Downloading...{idx + 1}/{len(video_links)}\nPercentage: {finished_length*10}%\nProgress: {progress}\n")
                except:
                    pass
                video_data,local_filename = await download_media(message.text, video_link, idx, 'video')
                
                if video_data:
                    with open(os.path.join(folder_name, local_filename), "wb") as file:
                        file.write(video_data)
                             
                await status.edit(f'Downloaded {idx + 1}/{len(video_links)}')
                time.sleep(.3)
            
            await status.edit('Uploading ....')
            zip_filename = f"{folder_name}.zip"
            shutil.make_archive(folder_name, 'zip', folder_name)

            await message.reply_document(open(zip_filename, "rb"), caption="Here are the videos! \n @BughunterBots")
            # await message.reply_video(local_filename)
            await status.delete()
            await txt.delete()
            shutil.rmtree(folder_name)
            await asyncio.sleep(1)
            os.remove(zip_filename)
            return

        else:
            await txt.edit(text=f"No Videos Found!!!", disable_web_page_preview=True)
            return

    except Exception as e:
        print(e)
        os.remove(zip_filename)
        error = f"ERROR: {(str(e))}"
        error_link = f"{REPO}/issues/new?title={quote(error)}"
        text = f'Something Bad occurred !!!\nCreate an issue here'
        issue_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Create Issue", url=error_link)]])
        await message.reply_text(text, disable_web_page_preview=True, quote=True, reply_markup=issue_markup)
        return e


async def all_pdf_scraping(query):
    try:
        message = query.message
        txt = await message.reply_text("Scraping url ...", quote=True)
        request, soup = await scrape(message.text)
        pdf_links = []

        for link in soup.find_all('a'):
            if 'href' in link.attrs and link['href'].endswith('.pdf'):
                pdf_links.append(link['href'])

        if len(pdf_links):
            txt = await txt.edit(text=f"Found {len(pdf_links)} Pdfs", disable_web_page_preview=True)
            status = await message.reply_text("Checking...", quote=True)
            folder_name = f"{message.chat.id}-pdfs"
            os.makedirs(folder_name, exist_ok=True)

            for idx, pdf_link in enumerate(pdf_links):
                progress, finished_length = await progress_bar(idx + 1, len(pdf_links))

                try:
                    await status.edit(f"Downloading...{idx + 1}/{len(pdf_links)}\nPercentage: {finished_length*10}%\nProgress: {progress}\n")
                except:
                    pass

                pdf_data = await download_pdf(message.text, pdf_link, idx, 'pdf')

                if pdf_data:
                    with open(os.path.join(folder_name), "wb") as file:
                        file.write(pdf_data)

                await status.edit(f'Downloaded {idx + 1}/{len(pdf_links)}')
                time.sleep(0.3)

            await status.edit('Uploading ....')
            zip_filename = f"{folder_name}.zip"
            shutil.make_archive(folder_name, 'zip', folder_name)

            await message.reply_document(open(zip_filename, "rb"), caption="Here are the Pdfs! \n @BughunterBots")
            await status.delete()
            await txt.delete()
            shutil.rmtree(folder_name)
            await asyncio.sleep(1)
            os.remove(zip_filename)
            return
        else:
            await txt.edit(text=f"No Pdf Found!!!", disable_web_page_preview=True)
            return

    except Exception as e:
        print(e)
        error = f"ERROR: {(str(e))}"
        error_link = f"{REPO}/issues/new?title={quote(error)}"
        text = f'Something Bad occurred !!!\nCreate an issue here'
        issue_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Create Issue", url=error_link)]])
        await message.reply_text(text, disable_web_page_preview=True, quote=True, reply_markup=issue_markup)
        return e
