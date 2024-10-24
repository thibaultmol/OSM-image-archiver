# OSM-image-archiver
## A quick project I threw togeher which has 3 scripts:

### [imgur_taginfo_to_url_list.py](imgur_taginfo_to_url_list.py)

Downloads all imgur links from Openstreetmap's Taginfo and saves to a txt file.
  
### [Download images.sh](Download%20images.sh)
Downloads the images that are in the txt file from the previous script

### [Do the imgur links still work.py](Do%20the%20imgur%20links%20still%20work.py)
This script checks to see if all the imgur urls in the file can still be accessed or if they've been deleted

## Snapshot of all images:

Twice a week using Github Actions the script is run to pull all the imgur urls from taginfo.
The latest version you can find here: [recent.txt](URL%20lists/recent.txt)

And here you can download the actual images (DO NOTE: I myself am not giving permission to use these images. Some of them have/had licenses on their respective Imgur pages which say what license applies to each one)

These downloads are based on the url list from 2024 10 25:

https://drive.proton.me/urls/AVGC7Q071W#UKyD62Tc0AHH

The amount of files is lower than the actual .txt file, because some urls were simply broken or deleted on Imgur's servers.
## Status of imgur links on OSM:
As of 2023 10 19 there are 26421 links but only 18 of them are broken. 4 of which were in this backup and will be recovered.
