import requests
from bs4 import BeautifulSoup
import os

# the base url is the root of the Sierra Chart docs, all pages are relative to this
base_url = "https://www.sierrachart.com/index.php?page=doc/"

pages_to_scrape = [
    "PriceGraphTypes.html",
    "doc_WorksheetStudy.html",
    "doc_VolumeByPrice.html",
    "doc_CreatingDLLs.html",
    "doc_ACSIL_Members_Variables_And_Arrays.html"
]

def scrape_sierra_chart_docs(pages_to_scrape):
    all_content = ""
    for page in pages_to_scrape:
        # build the full url, using the base url and the page name in pages_to_scrape
        url = base_url + page
        # get a soup object from the url with beautifulSoup
        soup = fetch_and_parse(url)
        # extract the relevant content from the soup object
        content = extract_content(soup)
        
        if page != pages_to_scrape[0]:
            all_content += "\n\n"
        
        # add the content to the all_content string, with a separator, this is to upload it easily to the output file
        all_content += f"--- {page} ---\n\n{content}"
    return all_content


def fetch_and_parse(url):
    response = requests.get(url)
    return BeautifulSoup(response.content, 'html.parser')


def extract_content(soup):
    content = ""
    content_div = soup.find('div', class_='content')

    if content_div:
        # Traverse the content_div and find all h1, h2, h3, and p tags
        for element in content_div.find_all(['h1', 'h2', 'h3', 'p', 'li']):
            if element.name == 'h1':
                content += f"# {element.get_text(strip=True)}\n\n"
            elif element.name == 'h2':
                content += f"## {element.get_text(strip=True)}\n\n"
            elif element.name == 'h3':
                content += f"### {element.get_text(strip=True)}\n\n"
            elif element.name == 'p' or element.name == 'li':
                content += f"{element.get_text(strip=True)}\n\n"

    return content


def main():
    # scrape the content from the pages
    content = scrape_sierra_chart_docs(pages_to_scrape)
    
    # Create the output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
    os.makedirs(output_dir, exist_ok=True)

    # Use os.path.join to create the file path
    output_file = os.path.join(output_dir, 'sierra-chart-docs-1.txt')

    # write the content to the output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    main()
