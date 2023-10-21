"""Script to extract Imgur URLs from OpenStreetMap taginfo data."""

import requests
import re

from datetime import datetime

def save_imgur_urls(imgur_urls, output_filename, all_output_filename):
    """Save the extracted Imgur URLs to a text file."""
    with open(output_filename, 'w', encoding='utf-8') as output_file:
        for url in imgur_urls:
            output_file.write(f"{url}\n")

    # Append to All_Imgur_urls.txt and remove duplicates
    all_urls = set()
    try:
        with open(all_output_filename, 'r', encoding='utf-8') as all_output_file:
            all_urls = set(line.strip() for line in all_output_file)
    except FileNotFoundError:
        pass

    all_urls.update(imgur_urls)
    
    with open(all_output_filename, 'w', encoding='utf-8') as all_output_file:
        for url in all_urls:
            all_output_file.write(f"{url}\n")


def download_json(url):
    """Download JSON data from a URL."""
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        return response.json()
    else:
        raise requests.RequestException(f"Failed to download JSON from {url}")

def process_data(data):
    """Process data to extract Imgur URLs."""
    imgur_urls = []
    for item in data:
        if 'imgur' in item['value']:
            urls = re.findall(
                r'(?:https?://)?(?:www\.)?(?:web\.archive\.org\/web\/\d{14}\/)?(i\.imgur\.com/[\w./?=&%-]+)',
                item['value']
            )
            for url in urls:
                full_url = f'https://{url}'
                full_url = re.sub(r'(\?.*)', '', full_url)  # Remove URL parameters
                full_url = re.sub(r'(_d\.webp)', '.webp', full_url)  # Replace "_d.webp" with ".webp"
                imgur_urls.append(full_url)
    return imgur_urls

def save_imgur_urls(imgur_urls, output_filename):
    """Save the extracted Imgur URLs to a text file."""
    with open(output_filename, 'w', encoding='utf-8') as output_file:
        for url in imgur_urls:
            output_file.write(f"{url}\n")

def main():
    """Main function to run the script."""
    base_url = (
        "https://taginfo.openstreetmap.org/api/4/search/by_value?"
        "query=imgur&sortname=count_all&sortorder=desc&rp=999&page="
    )

    # Define the filename using the current date
    output_filename = f"Snapshots/{datetime.now().strftime('%Y-%m-%d')}.txt"
    all_output_filename = "All_Imgur_urls.txt"

    imgur_urls = []
    page = 1

    while True:
        print(f"Processing Taginfo results page {page}...")
        url = f"{base_url}{page}"
        json_data = download_json(url)
        imgur_urls.extend(process_data(json_data["data"]))

        if json_data["page"] * json_data["rp"] >= json_data["total"]:
            break
        page += 1

    print(f"Saving Imgur URLs to {output_filename}...")
    save_imgur_urls(imgur_urls, output_filename, all_output_filename)
    print(f"Done! Imgur URLs saved in {output_filename}")


if __name__ == "__main__":
    main()
