import requests
from bs4 import BeautifulSoup
import os
import time
import itertools
from getpages import get_pages_to_scrape

# the base url is the root of the Sierra Chart docs, all pages are relative to this
# base_url = "https://www.sierrachart.com/index.php?page=doc/"
base_url = "https://www.sierrachart.com"

def scrape_sierra_chart_docs(pages_to_scrape, output_dir):
    total_pages = len(pages_to_scrape)
    log_file_path = os.path.join(output_dir, 'scrape_log.txt')
    max_words_per_file = 420000  # Maximum number of words per output file
    file_number = 1  # Starting file number
    current_content = ""  # Content for the current file
    current_word_count = 0  # Word count for the current file

    # Create a cycle iterator for the progress dots
    # dots_cycle = itertools.cycle(['.', '..', '...'])

    with open(log_file_path, 'w', encoding='utf-8') as log_file:
        for i, page in enumerate(pages_to_scrape, start=1):
            # dot = next(dots_cycle)
            print(f"Processing page {i}/{total_pages}: {page}")

            url = base_url + page

            try:
                soup = fetch_and_parse(url)
                content = extract_content(soup)
                status = "OK"
                log_file.write(f"{page} - {status}\n")
            except Exception as e:
                print(f"Error processing page {page}: {e}")
                content = ""
                status = "ERROR"
                log_file.write(f"{page} - {status}: {e}\n")
                continue  # Skip to the next page

            if content:
                # Add separator and page content
                page_content = f"--- {page} ---\n\n{content}\n\n"
                # Get word count of the page content
                word_count = len(content.split())
                current_word_count += word_count
                current_content += page_content

                # Check if current_word_count exceeds max_words_per_file
                if current_word_count >= max_words_per_file:
                    # Write current_content to file
                    output_file = os.path.join(output_dir, f'sierra-chart-docs-{file_number}.txt')
                    with open(output_file, "w", encoding="utf-8") as f:
                        f.write(current_content)
                    print(f"Saved {output_file} with {current_word_count} words.")
                    # Reset current_content and current_word_count
                    current_content = ""
                    current_word_count = 0
                    # Increment file_number
                    file_number += 1

            # Sleep for a short duration to avoid rate limiting
            time.sleep(0.8)  # Adjust the sleep time as needed

        # After processing all pages, write any remaining content to a file
        if current_content:
            output_file = os.path.join(output_dir, f'sierra-chart-docs-{file_number}.txt')
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(current_content)
            print(f"Saved {output_file} with {current_word_count} words.")

def fetch_and_parse(url):
    response = requests.get(url)
    response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
    return BeautifulSoup(response.content, 'html.parser')

def extract_content(soup):
    content = ""
    content_div = soup.find('div', class_='content')

    if content_div:
        # Traverse the content_div and find all h1, h2, h3, p, and li tags
        for element in content_div.find_all(['h1', 'h2', 'h3', 'p', 'li']):
            if element.name == 'h1':
                content += f"# {element.get_text(strip=True)}\n\n"
            elif element.name == 'h2':
                content += f"## {element.get_text(strip=True)}\n\n"
            elif element.name == 'h3':
                content += f"### {element.get_text(strip=True)}\n\n"
            elif element.name in ['p', 'li']:
                content += f"{element.get_text(strip=True)}\n\n"

    return content

def main():
    pages_to_scrape = get_pages_to_scrape()

    # Create the output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
    os.makedirs(output_dir, exist_ok=True)

    # Scrape the content from the pages
    scrape_sierra_chart_docs(pages_to_scrape, output_dir)

if __name__ == "__main__":
    main()
