"""
Scrapes a headline from The Daily Pennsylvanian website and saves it to a 
JSON file that tracks headlines over time.
"""

import os
import sys

import daily_event_monitor

import bs4
import requests
import loguru
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_most_read():
    """
    Scrapes the #1 most read article from The Daily Pennsylvanian home page.

    Returns:
        str: The headline text if found, otherwise an empty string.
    """
    url = "https://www.thedp.com"
    
    # Initialize the Selenium webdriver (Make sure chromedriver is installed)
    driver = webdriver.Chrome()  # or use webdriver.Firefox()
    driver.get(url)

    most_read_headline = ""

    try:
        # Wait until the most read section is loaded (timeout = 10 sec)
        most_read_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#mostRead a.frontpage-link.standard-link"))
        )

        # Get the text of the first most-read article
        most_read_headline = most_read_element.text
        most_read_link = most_read_element.get_attribute("href")

        print(f"Most Read Headline: {most_read_headline}")
        print(f"Most Read Link: {most_read_link}")

    except Exception as e:
        print(f"Error: {e}")
        most_read_headline = ""  # Return an empty string in case of error

    finally:
        driver.quit()  # Close the browser

    return most_read_headline



if __name__ == "__main__":
    # Setup logger to track runtime
    loguru.logger.add("scrape.log", rotation="1 day")

    # Create data dir if needed
    loguru.logger.info("Creating data directory if it does not exist")
    try:
        os.makedirs("data", exist_ok=True)
    except Exception as e:
        loguru.logger.error(f"Failed to create data directory: {e}")
        sys.exit(1)

    # Load daily event monitor
    loguru.logger.info("Loading daily event monitor")
    dem = daily_event_monitor.DailyEventMonitor("data/daily_pennsylvanian_headlines.json")

    # Run scrape for most-read article
    loguru.logger.info("Starting scrape for top most-read article")
    try:
        data_point = scrape_most_read()
    except Exception as e:
        loguru.logger.error(f"Failed to scrape data point: {e}")
        data_point = None

    # Save data if scrape was successful
    if data_point is not None:
        dem.add_today(data_point)
        dem.save()
        loguru.logger.info("Saved daily event monitor")

    # (Optional) Print tree and file contents for verification
    def print_tree(directory, ignore_dirs=[".git", "__pycache__"]):
        loguru.logger.info(f"Printing tree of files/dirs at {directory}")
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            level = root.replace(directory, "").count(os.sep)
            indent = " " * 4 * level
            loguru.logger.info(f"{indent}+--{os.path.basename(root)}/")
            sub_indent = " " * 4 * (level + 1)
            for file in files:
                loguru.logger.info(f"{sub_indent}+--{file}")

    print_tree(os.getcwd())

    loguru.logger.info("Printing contents of data file {}".format(dem.file_path))
    with open(dem.file_path, "r") as f:
        loguru.logger.info(f.read())

    loguru.logger.info("Scrape complete")
    loguru.logger.info("Exiting")
