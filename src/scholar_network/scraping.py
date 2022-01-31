"""This module contains information on scraping data from Google Scholar.

This module utilizes the `selenium` package to automate web scraping
and stores the scraped data in 'data/scraped.json' file.  It scrapes,
for each author_id provided, all of the publications for that author listed
on Google Scholar.  For each publication, the journal title and list of authors
are extracted.
"""
from selenium import webdriver
import time

from . import helpers


def get_publication_data(author_id: str, author_name: str = '') -> list[dict[str, str]]:
    """Retrives data from Google Scholar.

    This function is the primary web-utility that opens a new selenium
    window to automate visiting Google Scholar and extracting data.

    Args:
        author_id (str): Google Scholar ID of the author information to extract.

    Returns:
        list[dict[str, str]]: A list of publication data, each dictionary containing
        keys for the `journal_title` and `authors` both having string keys.
    """
    data = []
    profile_link = f"https://scholar.google.com/citations?&hl=en&user={author_id}"
    more_pubs = True
    loop = 0
    while more_pubs:
        print(f"Scraping {author_name.title()} page {loop + 1}")
        time.sleep(5)
        driver = webdriver.Safari()
        driver.get(f"{profile_link}&cstart={loop*100}&pagesize=100&view_op=list_works&sortby=pubdate")
        more_pubs = driver.find_element_by_id('gsc_bpf_more').is_enabled()
        if more_pubs:
            loop += 1
        pub_elements = driver.find_elements_by_css_selector("a.gsc_a_at")
        for pub in pub_elements:
            pub_info_link = pub.get_attribute("href")
            driver.get(pub_info_link)
            elements = driver.find_elements_by_class_name("gsc_oci_value")
            if len(elements) > 3:
                data.append(
                    {"authors": elements[0].text, "publication_year": elements[1].text, "journal_title": elements[2].text}
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
    pub_data = get_publication_data(scholar_id, scholar_name)
    helpers.append_pub_data_to_json(pub_data)
    print(f"Wrote {scholar_name if scholar_name else scholar_id} to file.")
