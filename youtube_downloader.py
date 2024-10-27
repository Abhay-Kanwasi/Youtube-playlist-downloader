import streamlit as st
import os
import yt_dlp
import tempfile
import zipfile
from pathlib import Path
import time

def get_best_download_link(video_url):
    """Get the direct download URL and info for a video"""
    ydl_opts = {
        'format': 'best[ext=mp4]/best',  # Prioritize MP4 format
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract video information
            info = ydl.extract_info(video_url, download=False)
            
            # Find the best MP4 format
            formats = info['formats']
            best_format = None
            
            # First try to find best MP4
            for f in formats:
                if f['ext'] == 'mp4' and (
                    not best_format or 
                    f.get('filesize', 0) > best_format.get('filesize', 0)
                ):
                    best_format = f
            
            # If no MP4 found, get the best available format
            if not best_format:
                best_format = formats[-1]
            
            return {
                'title': info['title'],
                'url': best_format['url'],
                'filesize': best_format.get('filesize', 0),
                'ext': best_format['ext'],
                'resolution': best_format.get('resolution', 'N/A')
            }
    except Exception as e:
        st.error(f"Error processing video: {str(e)}")
        return None

def process_playlist(playlist_url, start_index=1):
    """Process playlist and return video information"""
    ydl_opts = {
        'extract_flat': True,  # Don't download, just get metadata
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            playlist_info = ydl.extract_info(playlist_url, download=False)
            
            if 'entries' in playlist_info:
                # It's a playlist
                videos = []
                total_videos = len(playlist_info['entries'])
                
                with st.empty():
                    for idx, entry in enumerate(playlist_info['entries'][start_index-1:], start_index):
                        if entry:
                            st.write(f"Processing video {idx} of {total_videos}")
                            video_info = get_best_download_link(entry['url'])
                            if video_info:
                                videos.append(video_info)
                            time.sleep(0.5)  # Small delay to prevent rate limiting
                            
                return videos, playlist_info.get('title', 'Unknown Playlist')
            else:
                # Single video
                video_info = get_best_download_link(playlist_url)
                return [video_info] if video_info else [], 'Single Video'
    except Exception as e:
        st.error(f"Error processing playlist: {str(e)}")
        return [], 'Error'