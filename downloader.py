import yt_dlp
from io import BytesIO

def download_video(video_url):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
        'outtmpl': '%(title)s.%(ext)s',  # Temporary name
        'ignoreerrors': True,
        'verbose': True,
        'merge_output_format': 'mp4',
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        video_info = ydl.extract_info(video_url, download=False)  # Get info only
        video_title = video_info.get('title', 'Untitled Video')
        video_bytes = BytesIO()
        
        # Download video directly to memory
        ydl.download([video_url])  # Downloads the video
        video_bytes.seek(0)  # Reset pointer for download
        return video_bytes, f"{video_title}.mp4"

def get_playlist_videos(playlist_url, start_index=1):
    with yt_dlp.YoutubeDL({'extract_flat': 'in_playlist'}) as ydl:
        playlist_info = ydl.extract_info(playlist_url, download=False)
        videos = playlist_info['entries'][start_index - 1:]  # Select videos from the start index
    return videos
