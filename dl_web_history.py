import base64
import os
import re
import urllib.request
from urllib.parse import unquote

import py7zr
import requests


def create_onedrive_directdownload(onedrive_link):
    data_bytes64 = base64.b64encode(bytes(onedrive_link, "utf-8"))
    data_bytes64_String = (
        data_bytes64.decode("utf-8").replace("/", "_").replace("+", "-").rstrip("=")
    )
    resultUrl = (
        f"https://api.onedrive.com/v1.0/shares/u!{data_bytes64_String}/root/content"
    )
    return resultUrl


def get_link_file_size(direct_file_link):
    req = urllib.request.Request(direct_file_link, method="HEAD")
    f = urllib.request.urlopen(req)
    if f.status == 200:
        file_size = float(f.headers["Content-Length"])
        file_size = round(file_size / 1000000, 2)  # Change from bytes to megabytes
    else:
        file_size = None
    return file_size


def download(url: str, dest_folder: str):
    destination = os.path.join(os.getcwd(), dest_folder)
    if not os.path.exists(destination):
        os.makedirs(destination)  # create folder if it does not exist

    req = urllib.request.Request(url, method="HEAD")
    f = urllib.request.urlopen(req)
    filename = unquote((f.headers["Content-Disposition"].split("''"))[-1])

    filename = re.search('filename="(.*?)"', filename).group(1)
    file_path = os.path.join(destination, filename)

    if os.path.exists(file_path):
        # Delete the file if it already exists
        os.remove(file_path)

    r = requests.get(url, stream=True)
    if r.ok:
        print("Saving to:", os.path.abspath(file_path))
        with open(file_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:  # HTTP status code 4XX/5XX
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))
    return file_path


def download_onedrive_file(onedrive_link, dest_folder: str = None):
    if dest_folder is None:
        destination = os.path.dirname(os.path.abspath(__file__))
    else:
        destination = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), dest_folder
        )
    direct_file_link = create_onedrive_directdownload(onedrive_link)
    file_size = get_link_file_size(direct_file_link)
    file_path = download(direct_file_link, destination)
    return file_path, file_size


def extract_7z_file(archive_path: str):
    with py7zr.SevenZipFile(archive_path, "r") as archive:
        archive.extractall(os.path.dirname(archive_path))


def main(onedrive_link: str, dest_folder: str = "tmp"):
    history_url = onedrive_link
    browser_history_7z, browser_history_7z_size = download_onedrive_file(
        history_url, dest_folder
    )
    print(f"Downloaded {browser_history_7z_size} MB for browser history 7z archive.")
    extract_7z_file(browser_history_7z)
    print("Extracted browser history CSV file.")
    csv_file = os.path.join(os.path.dirname(browser_history_7z), "history_backup.csv")

    return csv_file


if __name__ == "__main__":
    csv_f = main(
        onedrive_link="https://1drv.ms/u/s!Aq-Pwiif__0FjJQA9rgZ1EVR4nUkLg?e=TDfaFi",
        dest_folder="assets",
    )
