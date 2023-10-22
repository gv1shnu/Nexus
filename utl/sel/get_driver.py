"""Chromedriver Download and Extraction"""

# Python standard libraries
import os
import time

# Third party libraries
from tqdm import tqdm as tqdm
import requests as requests
import zipfile

# Internal imports
from decl import CFT_URL, PLATFORM_NAME, CDR_PATH, OS_NAME
from src.helpers import get_soup, get_header
from utl.logger import Logger

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
                    return (f"https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/"
                            f"{v}/{PLATFORM_NAME}/chromedriver-{PLATFORM_NAME}.zip")
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


def unzip() -> bool:
    """
    Extract the Chromedriver executable from a ZIP archive.
    """
    zip_path = f"{CDR_PATH}/chromedriver.zip"
    target_folder = f"chromedriver-{PLATFORM_NAME}"
    exec_filename = "chromedriver" if OS_NAME == "Linux" else "chromedriver.exe"
    success = False
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file_info in zip_ref.infolist():
            if target_folder in file_info.filename and file_info.filename.endswith(exec_filename):
                # Extract the .exe file to the specified directory
                extract_path = os.path.join(CDR_PATH, os.path.basename(file_info.filename))
                with open(extract_path, 'wb') as extract_file:
                    extract_file.write(zip_ref.read(file_info.filename))
                logger.info(f"{exec_filename} extracted to {extract_path}")
                success = True
    if not success:
        logger.error(f"{exec_filename} not found in the ZIP file.")

    logger.debug('Deleting zip file')
    if success and os.path.exists(zip_path):
        os.remove(zip_path)
        logger.info(f"{zip_path} deleted.")
        return True
    else:
        logger.error(f"{zip_path} does not exist.")
        return False
