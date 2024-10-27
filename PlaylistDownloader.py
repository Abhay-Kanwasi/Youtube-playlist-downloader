import streamlit as st

from youtube_downloader import process_playlist



st.set_page_config(page_title="YouTube Downloader", page_icon="📥")

st.title("📥 YouTube Video Downloader")
st.markdown("""
### Instructions:
1. Paste a YouTube video or playlist URL
2. Click 'Get Download Links'
3. Use the download links to save videos directly to your device

⚠️ **Note**: Please respect YouTube's terms of service and copyright laws.
""")

# Get input from user
playlist_url = st.text_input("🔗 Enter YouTube URL:")
start_index = st.number_input("Start from video #:", min_value=1, value=1)

if st.button("🚀 Get Download Links"):
    if not playlist_url:
        st.warning("⚠️ Please enter a URL")

    
    with st.spinner("Processing..."):
        videos, playlist_title = process_playlist(playlist_url, start_index)
        
        if videos:
            st.success(f"✅ Found {len(videos)} videos in: {playlist_title}")
            
            # Display each video
            for i, video in enumerate(videos, start_index):
                with st.expander(f"🎥 {i}. {video['title']}", expanded=True):
                    cols = st.columns([2, 1])
                    
                    with cols[0]:
                        if video['resolution'] != 'N/A':
                            st.write(f"📺 Quality: {video['resolution']}")
                        if video['filesize']:
                            size_mb = video['filesize'] / (1024 * 1024)
                            st.write(f"📦 Size: {size_mb:.1f} MB")
                        st.write(f"🎬 Format: {video['ext']}")
                        
                    with cols[1]:
                        st.markdown(f"[Download Video]({video['url']})")
            
            st.info("""
            💡 **Download Tips:**
            - Click 'Download Video' to start downloading
            - Files will save to your default downloads folder
            - For large playlists, downloads might take some time
            """)
        else:
            st.error("❌ No videos found. Please check the URL and try again.")