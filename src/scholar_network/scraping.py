import csv
import json

from rich import pretty, print
from rich.progress import track
from selenium import webdriver

pretty.install()

ENCODING = "utf-8-sig"


def get_publication_data(web_driver, author_id):
    data = []
    profile_link = f"https://scholar.google.com/citations?user={author_id}&hl=en&oi=ao"
    web_driver.get(profile_link)
    pub_elements = web_driver.find_elements_by_css_selector("a.gsc_a_at")
    for pub in pub_elements:
        pub_info_link = pub.get_attribute("data-href")
        web_driver.get(f"https://scholar.google.com{pub_info_link}")
        elements = web_driver.find_elements_by_class_name("gsc_vcd_value")
        if len(elements) > 3:
            data.append(
                {"journal_title": elements[2].text, "authors": elements[0].text}
            )
        web_driver.back()
    return data


def get_author_ids_from_file():
    info = []
    with open("data/COPscholars.csv", "r", encoding=ENCODING) as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            cop_scholar_id = row["ID"]
            cop_scholar_name = row["Name"]
            info.append((cop_scholar_id, cop_scholar_name))
    return info


def write_author_to_json(author_name, author_info):
    with open("data/scraped.json", "r", encoding=ENCODING) as f:
        data = json.load(f)
    data[author_name] = author_info
    with open("data/scraped.json", "w", encoding=ENCODING) as f:
        json.dump(data, f, indent=4, sort_keys=True)


def get_single_author(scholar_id, scholar_name):
    driver = webdriver.Safari()
    pub_data = get_publication_data(driver, scholar_id)
    write_author_to_json(scholar_name, pub_data)
    print(f"Wrote {scholar_name} to file.")
    driver.close()


def scrape_scholars():
    main_driver = webdriver.Safari()
    author_ids = get_author_ids_from_file()
    for author in track(author_ids, total=len(author_ids)):
        with open("data/scraped.json", "r", encoding=ENCODING) as f:
            info = json.load(f)
        if not info.get(author[1]):
            # this is in a list of dicts which is fine for saving
            author_publication_data = get_publication_data(main_driver, author[0])
            # index 1 is name, so names will be our first json keys
            write_author_to_json(author[1], author_publication_data)
            print(f"Wrote {author[1]} to file.")
        else:
            print(f"Skipped {author[1]}")
    main_driver.close()


"""This skips authors that already have data! :)
So you can just keep re-running until it gets all of them.
"""
# if __name__ == "__main__":
#     scrape_scholars()
