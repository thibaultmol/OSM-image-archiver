#!/bin/bash

download_file() {
  url="$1"
  dir="downloaded_images"
  mkdir -p "$dir"
  file="$dir/$(basename "$url")"
  if [ ! -f "$file" ]; then
    echo "Downloading $url"
    curl -o "$file" "$url"
  else
    echo "Skipping $file, already downloaded"
  fi
}

export -f download_file

while read -r url; do
  while [ "$(jobs | wc -l)" -ge 5 ]; do
    sleep 1
  done

  download_file "$url" &
done < IMGURurls.txt
wait

echo "All downloads complete"
