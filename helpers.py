
import shutil
import requests
from utils import FINISHED_PROGRESS_STR, UN_FINISHED_PROGRESS_STR
import os

async def progress_bar(current, total):
    percentage = current / total
    finished_length = int(percentage * 10)
    unfinished_length = 10 - finished_length
    progress = f"{FINISHED_PROGRESS_STR * finished_length}{UN_FINISHED_PROGRESS_STR * unfinished_length}"
    return progress, finished_length

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


async def download_media(base_url, media_url, idx, media_type):
    try:
        with requests.get(media_url, stream=True) as response:
            response.raise_for_status()

            filename = os.path.basename(media_url)
            local_filename = f"{media_type}{idx}_{filename}"

            with open(local_filename, 'wb') as file:
                shutil.copyfileobj(response.raw, file)

            with open(local_filename, "rb") as file:
                media_data = file.read()

            os.remove(local_filename)
            return media_data,local_filename
    except Exception as e:
        print(f"Error downloading media from {media_url}: {e}")
        return None
    