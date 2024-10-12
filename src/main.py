import requests
from bs4 import BeautifulSoup
import os

# the base url is the root of the Sierra Chart docs, all pages are relative to this
base_url = "https://www.sierrachart.com/index.php?page=doc/"

pages_to_scrape = [
    "PriceGraphTypes.html",
    # "doc_WorksheetStudy.html",
    # "doc_VolumeByPrice.html",
    # "doc_CreatingDLLs.html",
    # "doc_ACSIL_Members_Variables_And_Arrays.html"
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
        # add the content to the all_content string, with a separator, this is to upload it easily to the output file
        all_content += f"\n\n--- {page} ---\n\n{content}"
    return all_content


def fetch_and_parse(url):
    response = requests.get(url)
    return BeautifulSoup(response.content, 'html.parser')


def extract_content(soup):
    content = ""
    
    # Find the div with class="content"
    content_div = soup.find('div', class_='content')
    
    if content_div:
        # Extract the title (h1 tag)
        title = content_div.find('h1')
        if title:
            content += f"# {title.get_text().strip()}\n\n"
        
        # Find all section tags with class="h2"
        sections = content_div.find_all('section', class_='h2')
        
        for section in sections:
            # Extract subheading (h2 tag)
            subheading = section.find('h2')
            if subheading:
                content += f"## {subheading.get_text().strip()}\n\n"
            
            # Remove the "[Link] - [Top]" element
            member_link = section.find('div', class_='member-link')
            if member_link:
                member_link.decompose()
            
            # Extract sub-subheadings (h3 tags) and their content
            for element in section.children:
                if element.name == 'section':
                    content += f"### {element.get_text().strip()}\n\n"
                elif element.get('class') and 'member-link' in element.get('class'):
                    # Skip this element as it's the "member-link" we want to ignore
                    continue
                elif element.name and element.name not in ['h2', 'h3', 'section']:
                    content += f"{element.name}: {element.get_text().strip()}\n\n"
    
    return content


def main():
    content = scrape_sierra_chart_docs(pages_to_scrape)
    with open("../output/sierra-chart-docs-1.txt", "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    main()
