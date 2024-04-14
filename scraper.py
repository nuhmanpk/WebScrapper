# /usr/bin/nuhmanpk/bughunter0 

import asyncio
import time
import requests
import os
import shutil
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import enums
from bs4 import BeautifulSoup
from urllib.parse import quote
from utils import REPO
from helpers import (
    download_image,
    download_media,
    download_pdf,
    init_headless_browser,
    progress_bar,
    progress_for_pyrogram
)
import imageio
from tqdm import tqdm


async def scrape(url):
    try:
        request = requests.get(url)
        soup = BeautifulSoup(request.content, "html5lib")
        return request, soup
    except Exception as e:
        print(e)
        return None, None


async def raw_data_scraping(query):
    try:
        message = query.message
        request, soup = await scrape(message.text)
        file_write = open(f"RawData-{message.chat.username}.txt", "a+")
        file_write.write(f"{request.content}")
        file_write.close()
        await message.reply_document(
            f"RawData-{message.chat.username}.txt",
            caption="©@BugHunterBots",
            quote=True,
        )
        await asyncio.sleep(1)
        os.remove(f"RawData-{message.chat.username}.txt")
        return
    except Exception as e:
        os.remove(f"RawData-{message.chat.username}.txt")
        error = f"ERROR: {(str(e))}"
        error_link = f"{REPO}/issues/new?title={quote(error)}"
        text = f"Something Bad occurred !!!\nCreate an issue here"
        issue_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Create Issue", url=error_link)]]
        )
        await message.reply_text(
            text, disable_web_page_preview=True, quote=True, reply_markup=issue_markup
        )
        return e


async def html_data_scraping(query):
    try:
        message = query.message
        request, soup = await scrape(message.text)
        file_write = open(f"HtmlData-{message.chat.username}.txt", "a+")
        soup.data = soup.prettify()
        file_write.write(f"{soup.data}")
        file_write.close()
        await message.reply_document(
            f"HtmlData-{message.chat.username}.txt",
            caption="©@BugHunterBots",
            quote=True,
        )
        await asyncio.sleep(1)
        os.remove(f"HtmlData-{message.chat.username}.txt")
    except Exception as e:
        os.remove(f"HtmlData-{message.chat.username}.txt")
        error = f"ERROR: {(str(e))}"
        error_link = f"{REPO}/issues/new?title={quote(error)}"
        text = f"Something Bad occurred !!!\nCreate an issue here"
        issue_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Create Issue", url=error_link)]]
        )
        await message.reply_text(
            text, disable_web_page_preview=True, quote=True, reply_markup=issue_markup
        )
        return e


async def all_links_scraping(query):
    try:
        message = query.message
        request, soup = await scrape(message.text)
        file_write = open(f"AllLinks-{message.chat.username}.txt", "a+")
        for link in soup.find_all("a"):
            links = link.get("href")
            file_write.write(f"{links}\n\n")
        file_write.close()
        await message.reply_document(
            f"AllLinks-{message.chat.username}.txt", caption="©@BugHunterBots"
        )
        await asyncio.sleep(1)
        os.remove(f"AllLinks-{message.chat.username}.txt")
    except Exception as e:
        os.remove(f"AllLinks-{message.chat.username}.txt")
        error = f"ERROR: {(str(e))}"
        error_link = f"{REPO}/issues/new?title={quote(error)}"
        text = f"Something Bad occurred !!!\nCreate an issue here"
        issue_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Create Issue", url=error_link)]]
        )
        await message.reply_text(
            text, disable_web_page_preview=True, quote=True, reply_markup=issue_markup
        )
        return e


async def all_paragraph_scraping(query):
    try:
        message = query.message
        request, soup = await scrape(message.text)
        file_write = open(f"AllParagraph-{message.chat.username}.txt", "a+")
        paragraph = ""
        for para in soup.find_all("p"):
            paragraph = para.get_text()
            file_write.write(f"{paragraph}\n\n")
        file_write.close()

        await message.reply_document(
            f"AllParagraph-{message.chat.username}.txt",
            caption="©@BugHunterBots",
            quote=True,
        )
        await asyncio.sleep(1)
        os.remove(f"AllParagraph-{message.chat.username}.txt")
    except Exception as e:
        os.remove(f"AllParagraph-{message.chat.username}.txt")
        error = f"ERROR: {(str(e))}"
        error_link = f"{REPO}/issues/new?title={quote(error)}"
        text = f"Something Bad occurred !!!\nCreate an issue here"
        issue_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Create Issue", url=error_link)]]
        )
        await message.reply_text(
            text, disable_web_page_preview=True, quote=True, reply_markup=issue_markup
        )
        return e


async def all_images_scraping(bot,query):
    try:
        message = query.message
        chat_id = message.chat.id
        txt = await message.reply_text("Scraping url ...", quote=True)
        request, soup = await scrape(message.text)
        image_links = []
        for img_tag in soup.find_all("img"):
            img_url = img_tag.get("src")
            image_links.append(img_url)

        text = await txt.edit(
            text=f"Found {len(image_links)} Images", disable_web_page_preview=True
        )

        if len(image_links):
            status = await message.reply_text("Checking...", quote=True)
            folder_name = f"{message.chat.id}-images"
            os.makedirs(folder_name, exist_ok=True)
            for idx, image_link in enumerate(image_links):
                image_data = await download_image(message.text, image_link, idx)
                if image_data:
                    with open(f"{folder_name}/image{idx}.jpg", "wb") as file:
                        file.write(image_data)
                    (
                        progress,
                        percentage,
                    ) = await progress_bar(idx + 1, len(image_links))
                    try:
                        await status.edit(
                            f"Downloding...\nPercentage: {percentage}%\nProgress: {progress}\n"
                        )
                    except:
                        pass
            await status.edit("Uploading ....")
            zip_filename = f"{message.chat.id}-images.zip"
            shutil.make_archive(folder_name, "zip", folder_name)
            c_time = time.time()
            await bot.send_chat_action(chat_id, enums.ChatAction.UPLOAD_PHOTO)
            await message.reply_document(
                open(zip_filename, "rb"),
                caption="Here are the images! \n @BUghunterBots",
                progress=progress_for_pyrogram,
                progress_args=('Uploading',status,c_time)  
            )
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
        text = f"Something Bad occurred !!!\nCreate an issue here"
        issue_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Create Issue", url=error_link)]]
        )
        await message.reply_text(
            text, disable_web_page_preview=True, quote=True, reply_markup=issue_markup
        )
        return e


async def all_audio_scraping(bot,query):
    try:
        message = query.message
        chat_id = message.chat.id
        txt = await message.reply_text("Scraping url ...", quote=True)
        request, soup = await scrape(message.text)
        audio_links = [link["src"] for link in soup.find_all("audio")]
        if len(audio_links):
            await txt.edit(
                text=f"Found {len(audio_links)} Images", disable_web_page_preview=True
            )
            status = await message.reply_text("Checking...", quote=True)
            folder_name = f"{message.chat.id}-audios"
            os.makedirs(folder_name, exist_ok=True)
            for idx, audio_link in enumerate(audio_links):
                audio_data = await download_media(
                    message.text, audio_link, idx, "audio"
                )
                if audio_data:
                    with open(f"{folder_name}/audio{idx}.jpg", "wb") as file:
                        file.write(audio_data)
                    progress, percentage = await progress_bar(idx + 1, len(audio_links))
                    try:
                        await status.edit(
                            f"Downloding...\nPercentage: {percentage}%\nProgress: {progress}\n"
                        )
                    except:
                        pass
                await status.edit(f"Downloaded {idx + 1}/{len(audio_links)}")
            await status.edit("Uploading ....")
            zip_filename = f"{message.chat.id}-audios.zip"
            shutil.make_archive(folder_name, "zip", folder_name)
            c_time = time.time()
            await bot.send_chat_action(chat_id, enums.ChatAction.UPLOAD_AUDIO)
            await message.reply_document(
                open(zip_filename, "rb"),
                caption="Here are the images! \n @BughunterBots",
                progress=progress_for_pyrogram,
                progress_args=('Uploading',status,c_time)  
            )
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
        text = f"Something Bad occurred !!!\nCreate an issue here"
        issue_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Create Issue", url=error_link)]]
        )
        await message.reply_text(
            text, disable_web_page_preview=True, quote=True, reply_markup=issue_markup
        )
        print(e)
        return e


async def all_video_scraping(bot,query):
    try:
        message = query.message
        chat_id = message.chat.id
        txt = await message.reply_text("Scraping url ...", quote=True)
        request, soup = await scrape(message.text)

        video_tags = soup.find_all("video")

        video_links = [
            video["src"] if video.has_attr("src") else video.find("source")["src"]
            for video in video_tags
        ]

        txt = await txt.edit(
            text=f"Found {len(video_links)} Videos", disable_web_page_preview=True
        )

        if len(video_links):
            status = await message.reply_text("Checking...", quote=True)
            folder_name = f"{message.chat.id}-videos"
            os.makedirs(folder_name, exist_ok=True)

            for idx, video_link in enumerate(video_links):
                progress, percentage = await progress_bar(idx + 1, len(video_links))

                try:
                    await status.edit(
                        f"Downloading...{idx + 1}/{len(video_links)}\nPercentage: {percentage}%\nProgress: {progress}\n"
                    )
                except:
                    pass
                video_data, local_filename = await download_media(
                    message.text, video_link, idx, "video"
                )

                if video_data:
                    with open(os.path.join(folder_name, local_filename), "wb") as file:
                        file.write(video_data)

                time.sleep(0.3)

            await status.edit("Uploading ....")
            zip_filename = f"{folder_name}.zip"
            shutil.make_archive(folder_name, "zip", folder_name)

            c_time = time.time()
            await bot.send_chat_action(chat_id, enums.ChatAction.UPLOAD_VIDEO)
            await message.reply_document(
                open(zip_filename, "rb"),
                caption="Here are the videos! \n @BughunterBots",
                progress=progress_for_pyrogram,
                progress_args=('Uploading',status,c_time)  
            )
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
        text = f"Something Bad occurred !!!\nCreate an issue here"
        issue_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Create Issue", url=error_link)]]
        )
        await message.reply_text(
            text, disable_web_page_preview=True, quote=True, reply_markup=issue_markup
        )
        return e


async def all_pdf_scraping(query):
    try:
        message = query.message
        txt = await message.reply_text("Scraping url ...", quote=True)
        request, soup = await scrape(message.text)
        pdf_links = []

        for link in soup.find_all("a"):
            if "href" in link.attrs and link["href"].endswith(".pdf"):
                pdf_links.append(link["href"])

        if len(pdf_links):
            txt = await txt.edit(
                text=f"Found {len(pdf_links)} Pdfs", disable_web_page_preview=True
            )
            status = await message.reply_text("Checking...", quote=True)
            folder_name = f"{message.chat.id}-pdfs"
            os.makedirs(folder_name, exist_ok=True)

            for idx, pdf_link in enumerate(pdf_links):
                progress, percentage = await progress_bar(idx + 1, len(pdf_links))

                try:
                    await status.edit(
                        f"Downloading...{idx + 1}/{len(pdf_links)}\nPercentage: {percentage}%\nProgress: {progress}\n"
                    )
                except:
                    pass

                pdf_data = await download_pdf(message.text, pdf_link, idx, "pdf")

                if pdf_data:
                    with open(os.path.join(folder_name), "wb") as file:
                        file.write(pdf_data)

                await status.edit(f"Downloaded {idx + 1}/{len(pdf_links)}")
                time.sleep(0.3)

            await status.edit("Uploading ....")
            zip_filename = f"{folder_name}.zip"
            shutil.make_archive(folder_name, "zip", folder_name)

            c_time = time.time()
            await message.reply_document(
                open(zip_filename, "rb"), caption="Here are the Pdfs! \n @BughunterBots",
                progress=progress_for_pyrogram,
                progress_args=('Uploading',status,c_time)  
            )
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
        text = f"Something Bad occurred !!!\nCreate an issue here"
        issue_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Create Issue", url=error_link)]]
        )
        await message.reply_text(
            text, disable_web_page_preview=True, quote=True, reply_markup=issue_markup
        )
        return e


async def extract_cookies(query):
    try:
        url = query.message.text
        message = query.message
        chat_id = message.chat.id
        txt = await message.reply_text("Initiating chrome Driver...", quote=True)
        driver = await init_headless_browser(url)

        await txt.edit("Getting cookies...")
        cookies = driver.get_cookies()
        await txt.edit("Preparing files...")
        file_write = open(f"Cookies-{chat_id}.txt", "a+")
        file_write.write(f"{cookies}")
        file_write.close()
        await txt.edit("Uploading...")
        await message.reply_document(
            f"Cookies-{chat_id}.txt", caption="©@BugHunterBots", quote=True
        )
        await asyncio.sleep(1)
        os.remove(f"Cookies-{chat_id}.txt")
        await txt.delete()
        return
    except Exception as e:
        os.remove(f"Cookies-{chat_id}.txt")
        error = f"ERROR: {(str(e))}"
        error_link = f"{REPO}/issues/new?title={quote(error)}"
        text = f"Something Bad occurred !!!\nCreate an issue here"
        issue_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Create Issue", url=error_link)]]
        )
        await message.reply_text(
            text, disable_web_page_preview=True, quote=True, reply_markup=issue_markup
        )
        return e


async def extract_local_storage(query):
    try:
        url = query.message.text
        message = query.message
        chat_id = message.chat.id
        txt = await message.reply_text("Initiating chrome Driver...", quote=True)
        driver = await init_headless_browser(url)
        local_storage_script = """
        var storage = {};
        for (var i = 0; i < localStorage.length; i++) {
            var key = localStorage.key(i);
            storage[key] = localStorage.getItem(key);
        }
        return storage;
        """
        await txt.edit("Executing script...")
        local_storage = driver.execute_script(local_storage_script)
        await txt.edit("Preparing files...")
        file_write = open(f"localStorage-{chat_id}.txt", "a+")
        file_write.write(f"{local_storage}")
        file_write.close()
        await txt.edit("Uploading...")
        await message.reply_document(
            f"localStorage-{chat_id}.txt", caption="©@BugHunterBots", quote=True
        )
        await asyncio.sleep(1)
        os.remove(f"localStorage-{chat_id}.txt")
        await txt.delete()
        return
    except Exception as e:
        os.remove(f"localStorage-{chat_id}.txt")
        error = f"ERROR: {(str(e))}"
        error_link = f"{REPO}/issues/new?title={quote(error)}"
        text = f"Something Bad occurred !!!\nCreate an issue here"
        issue_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Create Issue", url=error_link)]]
        )
        await message.reply_text(
            text, disable_web_page_preview=True, quote=True, reply_markup=issue_markup
        )
        return e


async def extract_metadata(query):
    try:
        message = query.message
        txt = await message.reply_text("Scraping url ...", quote=True)
        request, soup = await scrape(message.text)
        title = soup.title.string.strip() if soup.title else None
        description = soup.find("meta", attrs={"name": "description"})
        description = description["content"].strip() if description else None
        keywords = soup.find("meta", attrs={"name": "keywords"})
        keywords = keywords["content"].strip() if keywords else None

        metadata = {"title": title, "description": description, "keywords": keywords}

        metadata_text = "\n".join(
            [
                f"**{key.capitalize()}:** {value}"
                for key, value in metadata.items()
                if value
            ]
        )

        await message.reply_text(metadata_text)
        await txt.delete()
        return
    except Exception as e:
        error = f"ERROR: {(str(e))}"
        error_link = f"{REPO}/issues/new?title={quote(error)}"
        text = f"Something Bad occurred !!!\nCreate an issue here"
        issue_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Create Issue", url=error_link)]]
        )
        await message.reply_text(
            text, disable_web_page_preview=True, quote=True, reply_markup=issue_markup
        )
        return e


async def capture_screenshot(query):
    try:
        url = query.message.text
        message = query.message
        chat_id = message.chat.id
        txt = await message.reply_text("Initiating chrome Driver...", quote=True)
        driver = await init_headless_browser(url)

        time.sleep(2)
        await txt.edit("Taking screenshot...")
        screenshot_path = f"{chat_id}-screenshot.png"
        driver.save_screenshot(screenshot_path)
        driver.quit()
        await txt.edit("Uploading...")
        await message.reply_photo(screenshot_path, caption="@BughunterBots")
        await asyncio.sleep(1)
        await txt.delete()
        os.remove(screenshot_path)
        return
    except Exception as e:
        error = f"ERROR: {(str(e))}"
        error_link = f"{REPO}/issues/new?title={quote(error)}"
        text = f"Something Bad occurred !!!\nCreate an issue here"
        issue_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Create Issue", url=error_link)]]
        )
        await message.reply_text(
            text, disable_web_page_preview=True, quote=True, reply_markup=issue_markup
        )
        return e


async def record_screen(query, video_length=30, fps=30):
    try:
        url = query.message.text
        message = query.message
        chat_id = message.chat.id
        txt = await message.reply_text("Initiating chrome Driver...", quote=True)
        driver = await init_headless_browser(url)

        time.sleep(2)

        initial_scroll_height = driver.execute_script(
            "return document.body.scrollHeight;"
        )

        screenshot_dir = f"{chat_id}-screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)

        total_frames = int(video_length)
        await txt.edit("Capturing Screen...")
        for step in range(total_frames):
            fraction = step / total_frames
            scroll_height = int(fraction * initial_scroll_height)

            driver.execute_script(f"window.scrollTo(0, {scroll_height});")

            time.sleep(1 / fps)

            screenshot_path = os.path.join(screenshot_dir, f"screenshot_{step}.png")
            driver.save_screenshot(screenshot_path)

        driver.quit()
        time.sleep(2)

        await txt.edit("Converting to Video...")
        frame_duration = 0.3
        frames_per_screenshot = int(fps * frame_duration)
        video_path = f"{chat_id}-screen_record.mp4"

        with imageio.get_writer(video_path, fps=fps) as writer:
            for step in range(total_frames):
                screenshot_path = os.path.join(screenshot_dir, f"screenshot_{step}.png")
                image = imageio.imread(screenshot_path)

                for _ in range(frames_per_screenshot):
                    writer.append_data(image)

        for step in range(total_frames):
            screenshot_path = os.path.join(screenshot_dir, f"screenshot_{step}.png")
            os.remove(screenshot_path)

        os.rmdir(screenshot_dir)

        time.sleep(2)
        await txt.edit("Uploading...")
        await message.reply_video(video_path, caption="@BughunterBots")

        await asyncio.sleep(1)
        os.remove(video_path)
        await txt.delete()
        return
    except Exception as e:
        error = f"ERROR: {(str(e))}"
        error_link = f"{REPO}/issues/new?title={quote(error)}"
        text = f"Something Bad occurred !!!\nCreate an issue here"
        issue_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Create Issue", url=error_link)]]
        )
        await message.reply_text(
            text, disable_web_page_preview=True, quote=True, reply_markup=issue_markup
        )
        return e
