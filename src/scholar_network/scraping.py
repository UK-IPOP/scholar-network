"""This module contains information on scraping data from Google Scholar.

This module utilizes the `selenium` package to automate web scraping
and stores the scraped data in 'data/scraped.json' file.  It scrapes,
for each author_id provided, all of the publications for that author listed
on Google Scholar.  For each publication, the journal title and list of authors
are extracted.
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from . import helpers


def get_publication_data(author_id: str, author_name: str = '', preferred_browser: str = "safari") -> list[dict[str, str]]:
    """Retrieves data from Google Scholar.

    This function is the primary web-utility that opens a new selenium
    window to automate visiting Google Scholar and extracting data.

    Args:
        author_id (str): Google Scholar ID of the author information to extract.
        author_name (str, optional): Name of the scholar. Defaults to ''.
        preferred_browser (str, optional): Browser to use to scrape data. Must be one of 'chrome', 'firefox', or 'safari'. Defaults to "safari".

    Returns:
        list[dict[str, str]]: A list of publication data, each dictionary containing
        keys for the `journal_title` and `authors` both having string keys.
    """
    if preferred_browser == "chrome":
        browser = webdriver.Chrome
    elif preferred_browser == "firefox":
        browser = webdriver.Firefox
    elif preferred_browser == "safari":
        browser = webdriver.Safari
    else:
        raise ValueError("preferred_browser must be one of 'chrome', 'firefox', or 'safari'")
    data = []
    profile_link = f"https://scholar.google.com/citations?&hl=en&user={author_id}"
    more_pubs = True
    loop = 0
    while more_pubs:
        print(f"Scraping {author_name.title()} page {loop + 1}")
        time.sleep(5)
        driver = browser()
        driver.get(f"{profile_link}&cstart={loop*100}&pagesize=100&view_op=list_works&sortby=pubdate")
        more_pubs = driver.find_element(By.ID, 'gsc_bpf_more').is_enabled()
        if more_pubs:
            loop += 1
        pub_elements = driver.find_elements(By.CSS_SELECTOR, "a.gsc_a_at")
        for pub in pub_elements:
            pub_info_link = pub.get_attribute("href")
            driver.get(pub_info_link)
            elements = driver.find_elements(By.CLASS_NAME, "gsc_oci_value")
            # TODO: get link as well (class=gsc_oci_title_link)
            title_html = driver.find_element(By.CLASS_NAME, "gsc_oci_title_link")
            if len(elements) > 3:
                data.append(
                    {"authors": elements[0].text, "publication_year": elements[1].text, "journal_title": elements[2].text, "title": title_html.text}
                )
            driver.back()
        driver.close()
    return data


def scrape_single_author(scholar_id: str, scholar_name: str = '', preferred_browser: str = "safari"):
    """Scrapes data from google scholar and saves into json file.

    Args:
        scholar_id (str): Google Scholar ID of the author information to extract.
        scholar_name (str, optional): Name of the scholar. Defaults to ''.
        preferred_browser (str, optional): Browser to use to scrape data. Must be one of 'chrome', 'firefox', or 'safari'. Defaults to "safari".
    """
    pub_data = get_publication_data(scholar_id, scholar_name, preferred_browser)
    helpers.append_pub_data_to_json(pub_data)
    print(f"Wrote {scholar_name if scholar_name else scholar_id} to file.")
