## YouTube Playlist Downloader
This script extracts video links from a saved YouTube playlist HTML file and downloads them using yt-dlp. It supports parallel downloads and maintains a separate CSV log for each download folder to track downloaded videos.

### Installation
Clone or download this repository.
Install the required dependencies:
```bash
pip install yt-dlp beautifulsoup4 pandas termcolor
```
Usage
Save the YouTube playlist HTML:

Open the playlist page in your browser.
Right-click and select "Save As" to save the HTML file locally.
Run the script:

```bash
python playlist_downloader.py
```
### Provide inputs:

Enter the path to the saved HTML file when prompted. <br>
Specify the download folder name. This folder will be created if it doesn’t exist.
### Downloads and tracking:

Videos will be downloaded into the specified folder.
A CSV log (named <folder>_downloaded.csv) will be created inside the folder to track downloaded videos.
Example
```bash
Enter the path to the saved HTML file: path/to/playlist.html
Enter a folder name to save: my_downloads
```
Notes
Ensure you have a stable internet connection.
Avoid using special characters in folder names to prevent errors
