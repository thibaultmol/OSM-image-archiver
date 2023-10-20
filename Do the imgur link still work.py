import requests
import csv
from urllib.parse import urlparse, parse_qs

# Create the CSV header
with open('DoesItStillExistImgur.csv', 'w', newline='') as csvfile:
    fieldnames = ['Imgur_ID', 'Status']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

# Loop through each line in urls.txt
with open('urls.txt', 'r') as f:
    for line in f:
        line = line.strip()
        
        # Extract the Imgur ID from the URL
        parsed_url = urlparse(line)
        imgur_id = parsed_url.path.split('/')[-1].split('.')[0]

        # Check if the URL exists without downloading it
        try:
            response = requests.head(line, allow_redirects=False)
            status_code = response.status_code

            # Check the exit status of the request
            if status_code == 200:
                # URL exists
                status = 'Succeeds'
            else:
                # URL does not exist
                status = 'Not'
        except requests.RequestException:
            # URL does not exist or other error occurred
            status = 'Not'
        
        # Write to CSV
        with open('DoesItStillExistImgur.csv', 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'Imgur_ID': imgur_id, 'Status': status})
