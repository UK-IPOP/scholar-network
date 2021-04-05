from selenium import webdriver

from . import helpers

ENCODING = "utf-8-sig"


def get_publication_data(author_id: str) -> list[dict[str, str]]:
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


def scrape_single_author(scholar_id, scholar_name):
    pub_data = get_publication_data(scholar_id)
    helpers.append_pub_data_to_json(pub_data)
    print(f"Wrote {scholar_name} to file.")


def scrape_scholars(author_ids: list[str]):
    for author in author_ids:
        author_publication_data = get_publication_data(author)
        helpers.append_pub_data_to_json(author_publication_data)
        print(f"Wrote {author} to file.")
