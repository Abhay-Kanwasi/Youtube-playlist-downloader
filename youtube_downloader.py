import streamlit as st
import yt_dlp

def get_best_download_link(video_url):
    """
    Gets direct download link for a single video with better format handling
    """
    ydl_opts = {
        'format': 'best[ext=mp4]/best',  # Prefer MP4, but accept best available
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,  # We need full info
        'youtube_include_dash_manifest': False,  # Avoid DASH formats
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Get video info
            info = ydl.extract_info(video_url, download=False)
            
            # Sometimes the video info is nested
            if 'entries' in info:
                info = info['entries'][0]
            
            # Get the URL directly from the selected format
            url = info.get('url', None)
            
            # If direct URL not found, try getting it from formats
            if not url and 'formats' in info:
                # Filter for MP4 formats first
                mp4_formats = [f for f in info['formats'] 
                             if f.get('ext', '') == 'mp4' and f.get('url')]
                
                if mp4_formats:
                    # Get the best quality MP4
                    best_format = max(mp4_formats, 
                                    key=lambda f: f.get('filesize', 0) or f.get('width', 0) or 0)
                else:
                    # If no MP4, get the best available format
                    best_format = max(info['formats'], 
                                    key=lambda f: f.get('filesize', 0) or f.get('width', 0) or 0)
                
                url = best_format.get('url')
                
            if not url:
                raise Exception("No downloadable URL found")
                
            return {
                'title': info.get('title', 'Untitled Video'),
                'url': url,
                'filesize': info.get('filesize', 0),
                'resolution': info.get('resolution', 'N/A'),
                'ext': info.get('ext', 'mp4')
            }
            
    except Exception as e:
        st.error(f"Error processing video: {str(e)}")
        return None

def process_playlist(playlist_url, start_index=1):
    """
    Process playlist and return video information
    """
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,  # Only get video URLs initially
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Get playlist info
            playlist_info = ydl.extract_info(playlist_url, download=False)
            
            if 'entries' in playlist_info:
                # It's a playlist
                videos = []
                total_videos = len(playlist_info['entries'])
                
                # Create a progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Process each video
                for idx, entry in enumerate(playlist_info['entries'][start_index-1:], start_index):
                    if entry:
                        # Update status
                        status = f"Processing video {idx} of {total_videos}"
                        status_text.text(status)
                        progress_bar.progress(idx/total_videos)
                        
                        # Get video URL
                        video_url = entry.get('url', None)
                        if not video_url and 'id' in entry:
                            video_url = f"https://www.youtube.com/watch?v={entry['id']}"
                        
                        if video_url:
                            video_info = get_best_download_link(video_url)
                            if video_info:
                                videos.append(video_info)
                
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()
                
                return videos, playlist_info.get('title', 'Unknown Playlist')
            else:
                # Single video
                video_info = get_best_download_link(playlist_url)
                return [video_info] if video_info else [], 'Single Video'
                
    except Exception as e:
        st.error(f"Error processing playlist: {str(e)}")
        return [], 'Error'

