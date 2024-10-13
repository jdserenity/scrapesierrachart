import requests
from bs4 import BeautifulSoup
import os
import re

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
        all_content += f"--- {page} ---\n\n{content}"
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
            
            # Remove the "[Link] - [Top]" element from the h2's
            member_link = section.find('div', class_='member-link')
            if member_link:
                member_link.decompose()

            for descendant in section.descendants:        
                if 'section' in str(descendant):
                    content += f"{extract_h3_content(str(descendant))}\n\n"
                    content += f"{extract_p_content(str(descendant))}\n\n"
    
    return content


def extract_h3_content(text):
    start_index = text.find('<h3')
    if start_index == -1:
        return ""
    
    new_start_index = text.find('>', start_index)
    new_start_index += 1
    end_index = text.find('</h3>', new_start_index)
    # end_index += 5

    return '### ' + text[new_start_index:end_index]
    


def extract_p_content(text):
    start_index = text.find('<p>')
    if start_index == -1:
        return ""  # Return empty string if <p> is not found
    
    start_index += 3  # Move past '<p>'
    end_index = text.find('</p>', start_index)

    content = ""
    
    if end_index == -1:
        content = text[start_index:]  # Get rest of string if </p> is not found
    else:
        content = text[start_index:end_index]
    
    # Remove <b> and </b> tags
    content = content.replace('<b>', '').replace('</b>', '')
    
    # Remove content inside <img> tags
    while '<img' in content:
        img_start = content.find('<img')
        img_end = content.find('>', img_start)
        if img_end != -1:
            content = content[:img_start] + content[img_end + 1:]
        else:
            break
    
    # Remove content inside <a> tags
    while '<a' in content:
        a_start = content.find('<a')
        a_end = content.find('</a>', a_start)
        if a_end != -1:
            content = content[:a_start] + content[a_end + 4:]
        else:
            break

    # Remove content inside <div> tags
    while '<div' in content:
        div_start = content.find('<div')
        div_end = content.find('</div>', div_start)
        if div_end != -1:
            content = content[:div_start] + content[div_end + 6:]
        else:
            break
    
    return content


def remove_excess_newlines(text):
    # Replace more than two consecutive newlines with two newlines
    return re.sub(r'\n{3,}', '\n\n', text)


def main():
    # scrape the content from the pages
    content = scrape_sierra_chart_docs(pages_to_scrape)
    
    # Remove excess newlines
    content = remove_excess_newlines(content)
    
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
