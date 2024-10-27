import streamlit as st
from downloader import download_video, get_playlist_videos

st.title("YouTube Playlist Downloader")

# Input fields
playlist_url = st.text_input("Enter the YouTube playlist URL:")
playlist_start = st.number_input("Start from video number:", min_value=1, value=1, step=1)

# Download button
if st.button("Download Playlist"):
    if playlist_url:
        st.write("Fetching playlist info...")
        videos = get_playlist_videos(playlist_url, start_index=playlist_start)
        
        for index, video in enumerate(videos, start=playlist_start):
            st.write(f"Preparing to download video {index}: {video.get('title')}")
            video_bytes, video_filename = download_video(video['url'])
            st.download_button(label=f"Download {video.get('title')}", data=video_bytes, file_name=video_filename)
    else:
        st.error("Please enter a valid playlist URL.")
