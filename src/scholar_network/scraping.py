"""This module contains information on scraping data from Google Scholar.

This module utilizes the `selenium` package to automate web scraping
and stores the scraped data in 'data/scraped.json' file.  It scrapes,
for each author_id provided, all of the publications for that author listed
on Google Scholar.  For each publication, the journal title and list of authors
are extracted.
"""
from selenium import webdriver

from . import helpers


def get_publication_data(author_id: str) -> list[dict[str, str]]:
    """Retrives data from Google Scholar.

    This function is the primary web-utility that opens a new selenium
    window to automate visiting Google Scholar and extracting data.

    Args:
        author_id (str): Google Scholar ID of the author information to extract.

    Returns:
        list[dict[str, str]]: A list of publication data, each dictionary containing
        keys for the `journal_title` and `authors` both having string keys.
    """
    driver = webdriver.Safari()
    data = []
    profile_link = f"https://scholar.google.com/citations?user={author_id}&hl=en&oi=ao"
    driver.get(profile_link)
    pub_elements = driver.find_elements_by_css_selector("a.gsc_a_at")
    for pub in pub_elements:
        pub_info_link = pub.get_attribute("data-href")
        driver.get(f"https://scholar.google.com{pub_info_link}")
        elements = driver.find_elements_by_class_name("gsc_vcd_value")
        if len(elements) > 3:
            data.append(
                {"journal_title": elements[2].text, "authors": elements[0].text}
            )
        driver.back()
    driver.close()
    return data


def scrape_single_author(scholar_id: str, scholar_name: str = ''):
    """Scrapes data from google scholar and saves into json file.

    Args:
        scholar_id (str): Google Scholar ID of the author information to extract.
        scholar_name (str, optional): Name of the scholar. Defaults to ''.
    """
    pub_data = get_publication_data(scholar_id)
    helpers.append_pub_data_to_json(pub_data)
    print(f"Wrote {scholar_name if scholar_name else scholar_id} to file.")
