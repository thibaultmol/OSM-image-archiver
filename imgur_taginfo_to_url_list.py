"""Script to extract Imgur URLs from OpenStreetMap taginfo data."""

import re
import requests

def download_json(url):
    """Download JSON data from a URL."""
    # Send an HTTP GET request with a 10-second timeout
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
            # Use regex to get imgur url even if it's prefixed by an archive.org url
            urls = re.findall(
                r'(?:https?://)?(?:www\.)?(?:web\.archive\.org\/web\/\d{14}\/)?(i\.imgur\.com/[\w./?=&%-]+)',
                item['value']
            )
            for url in urls:
                # Prepend 'https://' to the extracted Imgur URL
                full_url = f'https://{url}'
                imgur_urls.append(full_url)
    return imgur_urls

def save_imgur_urls(imgur_urls, output_filename):
    """Save the extracted Imgur URLs to a text file."""
    # Open the output file with utf-8 encoding
    with open(output_filename, 'w', encoding='utf-8') as output_file:
        for url in imgur_urls:
            # Write each Imgur URL to the output file, followed by a newline
            output_file.write(f"{url}\n")

def main():
    """Main function to run the script."""
    base_url = (
        "https://taginfo.openstreetmap.org/api/4/search/by_value?"
        "query=imgur&sortname=count_all&sortorder=desc&rp=999&page="
    )
    output_filename = "IMGURurls.txt"

    imgur_urls = []
    page = 1

    while True:
        url = f"{base_url}{page}"
        json_data = download_json(url)
        imgur_urls.extend(process_data(json_data["data"]))

        # Check if the current page is the last page, and if so, break the loop
        if json_data["page"] * json_data["rp"] >= json_data["total"]:
            break
        page += 1

    save_imgur_urls(imgur_urls, output_filename)

if __name__ == "__main__":
    main()
