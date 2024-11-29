import yt_dlp
import pandas as pd
import os
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from termcolor import colored

def get_playlist_links_from_file(html_file_path):
    with open(html_file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
    
    # Extract video links and titles
    video_data = []
    for link in soup.find_all('a', class_='yt-simple-endpoint style-scope ytd-playlist-video-renderer'):
        href = link.get('href')
        title = link.get('title')
        if href and title:
            full_url = f'{href.split("&")[0]}'
            video_data.append({'title': title, 'link': full_url})
    
    return video_data  # Returns a list of dictionaries

def download_video(video_url, download_folder, csv_file):
    try:
        df = pd.read_csv(csv_file)
        if video_url in df['link'].values:
            print(colored(f"✔ Already downloaded: {video_url}", 'yellow'))
            return
        
        ydl_opts = {
            'outtmpl': f'{download_folder}/%(title)s.%(ext)s',
            'quiet': True,  # Suppress detailed output
            'no_warnings': True,  # Hide warnings
            'format': 'best',
            'progress_hooks': [progress_hook],  # Attach progress hook
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        
        # Mark as downloaded in the folder-specific CSV
        new_row = pd.DataFrame({'link': [video_url], 'title': [video_url]})
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(csv_file, index=False)
        
        print(colored(f"✔ Downloaded: {video_url}", 'green'))
    except Exception as e:
        print(colored(f"✘ Error downloading {video_url}: {e}", 'red'))

def progress_hook(d):
    if d['status'] == 'finished':
        print(colored("\n✔ Download complete.", 'cyan'))
    elif d['status'] == 'downloading':
        print(f"\r⏳ Downloading: {d['_percent_str']} at {d['_speed_str']}", end='', flush=True)

# Main function to manage downloads
def main():
    html_file_path = input("Enter the path to the saved HTML file: ")
    download_folder = input("Enter a folder name to save: ")
    csv_file = os.path.join(download_folder, f"{download_folder}_downloaded.csv")  # Folder-specific CSV
    
    # Create download folder and CSV file if they don't exist
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    if not os.path.exists(csv_file):
        pd.DataFrame(columns=['link', 'title']).to_csv(csv_file, index=False)
    
    video_links = get_playlist_links_from_file(html_file_path)
    print(f"🔍 Total videos found: {len(video_links)}")
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(lambda video: download_video(video['link'], download_folder, csv_file), video_links)

if __name__ == "__main__":
    main()
