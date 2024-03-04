"""Script to extract Imgur URLs from OpenStreetMap taginfo data."""

import requests
import re
import os
from datetime import datetime

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

def merge_and_deduplicate(new_urls, recent_filename):
    """Merge and deduplicate Imgur URLs with the recent.txt file."""
    if os.path.exists(recent_filename):
        with open(recent_filename, 'r', encoding='utf-8') as file:
            existing_urls = file.read().splitlines()
    else:
        existing_urls = []

    all_urls = list(set(existing_urls + new_urls))  # Merge and remove duplicates
    all_urls.sort()  # Optional: Sort the URLs
    return all_urls

def save_imgur_urls(imgur_urls, output_directory, base_filename):
    """Save the extracted Imgur URLs to a text file and update recent.txt."""
    today = datetime.now().strftime("%Y %m %d")
    output_filename = os.path.join(output_directory, f"{base_filename} as of {today}.txt")
    recent_filename = os.path.join(output_directory, "recent.txt")

    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    all_urls = merge_and_deduplicate(imgur_urls, recent_filename)

    # Save to the timestamped output file
    with open(output_filename, 'w', encoding='utf-8') as output_file:
        for url in all_urls:
            output_file.write(f"{url}\n")

    # Overwrite recent.txt with the new data
    with open(recent_filename, 'w', encoding='utf-8') as recent_file:
        for url in all_urls:
            recent_file.write(f"{url}\n")

def main():
    """Main function to run the script."""
    base_url = (
        "https://taginfo.openstreetmap.org/api/4/search/by_value?"
        "query=imgur&sortname=count_all&sortorder=desc&rp=999&page="
    )
    output_directory = "URL lists"
    base_filename = "all IMGUR urls"

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

    print(f"Saving Imgur URLs...")
    save_imgur_urls(imgur_urls, output_directory, base_filename)
    print("Done! Imgur URLs updated.")

if __name__ == "__main__":
    main()
