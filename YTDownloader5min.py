import sys
import yt_dlp
import os

# Function to safely show a message to the user
def show_message(message):
    print(f"\n{message}\n")

def download_video(url):
    """
    Downloads the first 5 minutes of a YouTube video from the given URL.
    """
    try:
        #testing my push function
        # Define the download options
        ydl_opts = {
            # Select the single best format that contains both video and audio.
            'format': 'best',
            # Template for the output filename
            'outtmpl': '%(title)s.%(ext)s',
            # Download only the first 5 minutes of the video
            'download_sections': ['*00:00:00-00:05:00'],
            'progress_hooks': [show_progress]
        }

        # Initialize the downloader with the specified options
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Check if the URL is valid before attempting to download
            info_dict = ydl.extract_info(url, download=False)
            if 'entries' in info_dict:
                show_message("Playlist detected. Downloading the first video only.")
                url = info_dict['entries'][0]['webpage_url']

            show_message(f"Starting download for: {info_dict.get('title', 'Unknown Title')}")
            ydl.download([url])
            show_message("Download complete!")

    except yt_dlp.utils.DownloadError as e:
        show_message(f"Error during download: {e}")
    except Exception as e:
        show_message(f"An unexpected error occurred: {e}")

def show_progress(d):
    """
    A progress hook to display download status.
    """
    if d['status'] == 'downloading':
        # Get the total file size if available
        total_bytes = d.get('total_bytes')
        downloaded_bytes = d.get('downloaded_bytes')
        
        if total_bytes and downloaded_bytes:
            percentage = downloaded_bytes / total_bytes * 100
            print(f"Downloading: {percentage:.2f}%", end="\r")
    elif d['status'] == 'finished':
        print("Download finished. Processing file...", end="\r")

if __name__ == "__main__":
    # Check if a URL was provided as a command-line argument
    if len(sys.argv) < 2:
        show_message("Usage: python downloader.py \"[youtube_url]\"")
    else:
        video_url = sys.argv[1]
        download_video(video_url)