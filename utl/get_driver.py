"""Chromedriver Download and Extraction"""

import os
import time
from tqdm import tqdm as tqdm
import requests as requests
import zipfile
from src.helpers import get_soup, get_header
from utl.logger import Logger

CFT_URL = "https://googlechromelabs.github.io/chrome-for-testing/"
logger = Logger()


def get_chromedriver_url() -> str or None:
    """
    Get the download URL for linux Chromedriver.

    Returns:
        str or None: Download URL for Chromedriver if found, otherwise None.
    """
    try:
        soup = get_soup(CFT_URL)
        if soup:
            data1 = soup.find('section', id="stable")
            if data1:
                version = data1.find('code')
                if version:
                    v = str(version)[6:-7]
                    return f"https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/{v}/linux64/chromedriver-linux64.zip"
    except Exception as e:
        logger.error(f"An error occurred while getting downloading link for chromedriver: {e}")
        return None


def download(url: str, download_folder: str, name: str) -> bool:
    """
    Download a file from the given URL.

    Args:
        url (str): URL of the file to download.
        download_folder (str): Directory to save the downloaded file.
        name (str): Name of the downloaded file.
    """
    if not os.path.exists(download_folder):
        os.mkdir(download_folder)
    # download the body of response by chunk, not immediately
    try:
        response = requests.get(url, stream=True, headers=get_header())
    except requests.exceptions.ConnectionError:
        time.sleep(10)
        response = requests.get(url, stream=True, headers=get_header())
    if response and response.status_code == 200:
        # get the total file size
        file_size = int(response.headers.get("Content-Length", 0))
        # get the file name
        filename = os.path.join(download_folder, name)
        # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
        progress = tqdm(response.iter_content(1024), f"Downloading {filename}", total=file_size, unit="B",
                        unit_scale=True,
                        unit_divisor=1024)
        with open(filename, "wb") as f:
            for data in progress:
                # write data read to the file
                f.write(data)
                # update the progress bar manually
                progress.update(len(data))
        logger.info(f"File downloaded successfully")
        return True
    else:
        logger.error(f"Failed to access file: {url}")
        return False


def unzip(zip_path: str, extract_dir: str, platform: str) -> bool:
    """
    Extract the Chromedriver executable from a ZIP archive.

    Args:
        zip_path (str): Path to the ZIP archive.
        extract_dir (str): Directory to extract the executable to.
        platform (str): Platform identifier ("linux64", "win64").
    """
    target_folder = f"chromedriver-linux64"
    exec_filename = "chromedriver"
    success = False
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file_info in zip_ref.infolist():
            if target_folder in file_info.filename and file_info.filename.endswith(exec_filename):
                # Extract the .exe file to the specified directory
                extract_path = os.path.join(extract_dir, os.path.basename(file_info.filename))
                with open(extract_path, 'wb') as extract_file:
                    extract_file.write(zip_ref.read(file_info.filename))
                logger.info(f"{exec_filename} extracted to {extract_path}")
                success = True
                break
    if not success:
        logger.error(f"{exec_filename} not found in the ZIP file.")
        return False

    logger.debug('Deleting zip file')
    if success and os.path.exists(zip_path):
        os.remove(zip_path)
        logger.info(f"{zip_path} deleted.")
        return True
    else:
        logger.error(f"{zip_path} does not exist.")
        return False
