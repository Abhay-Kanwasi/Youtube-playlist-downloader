import yt_dlp
from io import BytesIO
import tempfile
import os

def download_video(video_url):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
        'merge_output_format': 'mp4',
        'ignoreerrors': True,
        'verbose': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Create a temporary file to download video
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            ydl_opts['outtmpl'] = temp_file.name
            ydl.download([video_url])
            
            # Read the video file into memory
            with open(temp_file.name, "rb") as f:
                video_data = BytesIO(f.read())
            
            # Get video title and return data in memory
            video_info = ydl.extract_info(video_url, download=False)
            video_title = video_info.get('title', 'Untitled Video')
            
            # Clean up temporary file
            os.remove(temp_file.name)

        video_data.seek(0)
        return video_data, f"{video_title}.mp4"

def get_playlist_videos(playlist_url, start_index=1):
    with yt_dlp.YoutubeDL({'extract_flat': 'in_playlist'}) as ydl:
        playlist_info = ydl.extract_info(playlist_url, download=False)
        videos = playlist_info['entries'][start_index - 1:]
    return videos
