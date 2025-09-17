import sys
import yt_dlp
import os

# Function to safely show a message to the user
def show_message(message):
    """Prints a formatted message to the console."""
    print(f"\n{message}\n")

def show_progress(d):
    """
    An improved progress hook to display download status with more details.
    This function is called by yt-dlp during the download process.
    """
    if d['status'] == 'downloading':
        # Extract progress info from the dictionary provided by yt-dlp
        percent_str = d.get('_percent_str', 'N/A').strip()
        speed_str = d.get('_speed_str', 'N/A').strip()
        eta_str = d.get('_eta_str', 'N/A').strip()
        
        # Create a clean, single-line output string
        progress_line = f"Downloading: {percent_str} | Speed: {speed_str} | ETA: {eta_str}"
        
        # Print the progress line, using carriage return to overwrite the previous line
        # The padding at the end ensures the previous line is fully cleared
        sys.stdout.write(f"\r{progress_line:<80}")
        sys.stdout.flush()
        
    elif d['status'] == 'finished':
        # When downloading is finished, print a final message and a newline
        sys.stdout.write("\n\nDownload finished. Merging formats...\n")
        sys.stdout.flush()

def download_video(url):
    """
    Downloads a YouTube video using yt-dlp.
    It prioritizes 1080p resolution and merges the best video and audio into an MP4 file.
    """
    try:
        # Define the download options for yt-dlp
        ydl_opts = {
            # Select the best video up to 1080p and the best audio, then merge them.
            # Fallback to the best pre-merged file if separate streams aren't available.
            'format': 'bestvideo[height<=1080]+bestaudio/best',
            
            # Use the video's title for the output filename.
            'outtmpl': '%(title)s.%(ext)s',
            
            # Ensure the final merged file is in the MP4 container format.
            'merge_output_format': 'mp4',
            
            # Use a cookies file to handle age-restricted or members-only content.
            'cookiefile': 'cookies.txt',
            
            # Register our custom function to show progress.
            'progress_hooks': [show_progress] 
        }

        # Initialize the downloader with our specified options
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # First, extract info without downloading to check for playlists
            info_dict = ydl.extract_info(url, download=False)
            
            # If the URL is a playlist, handle it
            if 'entries' in info_dict:
                show_message("Playlist detected. Downloading the first video only.")
                # Get the URL of the first video in the playlist
                url = info_dict['entries'][0]['webpage_url']
                # Re-extract info for just the single video to get its title correctly
                info_dict = ydl.extract_info(url, download=False)

            show_message(f"Starting download for: {info_dict.get('title', 'Unknown Title')}")
            
            # Start the actual download
            ydl.download([url])
            
            show_message("✅ Download complete!")

    except yt_dlp.utils.DownloadError as e:
        show_message(f"❌ Error during download: {e}")
    except Exception as e:
        show_message(f"❌ An unexpected error occurred: {e}")

# This block runs when the script is executed directly from the command line
if __name__ == "__main__":
    # Check if a URL was provided as a command-line argument
    if len(sys.argv) < 2:
        show_message("Usage: python YTDownloader.py \"<YouTube_URL>\"")
        show_message("Please provide a video URL.")
        sys.exit(1)
    
    # Get the URL from the command-line arguments
    video_url = sys.argv[1]
    
    # Call the main download function
    download_video(video_url)