import requests
from bs4 import BeautifulSoup
import os

def get_pages_to_scrape():
    pages_to_scrape = []

    url = "https://www.sierrachart.com/index.php?page=doc/Contents.php"

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    sections = soup.find_all('section', class_='h3')

    for section in sections:
        pages_to_scrape.extend([a['href'] for a in section.find_all('a') if 'index.php?page=doc/' in a['href']])

    return pages_to_scrape


def main():
    pages_to_scrape = get_pages_to_scrape()
    
    # Create the output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
    os.makedirs(output_dir, exist_ok=True)

    # Use os.path.join to create the file path
    output_file = os.path.join(output_dir, 'pages_to_scrape.txt')

    with open(output_file, 'w') as f:
        for page in pages_to_scrape:
            f.write(page + '\n')


if __name__ == "__main__":
    main()

# print(len(pages_to_scrape))
# print(pages_to_scrape[0])
# print(pages_to_scrape[-1])