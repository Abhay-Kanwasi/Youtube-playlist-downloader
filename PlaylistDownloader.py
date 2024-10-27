import streamlit as st

from youtube_downloader import process_playlist



st.set_page_config(
    page_title="YouTube Playlist Downloader",
    page_icon="📥",
    layout="wide"
)

st.title("📥 YouTube Playlist Downloader")

# Add some nice styling
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
    }
    .video-container {
        border: 1px solid #ddd;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
### Instructions:
1. Enter a YouTube playlist URL below
2. Choose which video to start from
3. Click 'Get Download Links'
4. Click on the download links to save videos directly to your device

⚠️ **Note**: Please respect YouTube's terms of service and copyright laws.
""")

# User inputs
playlist_url = st.text_input("🔗 Enter YouTube Playlist URL:")
col1, col2 = st.columns([3, 1])
with col2:
    start_index = st.number_input("Start from video #:", min_value=1, value=1)

if st.button("🚀 Get Download Links"):
    if not playlist_url:
        st.warning("⚠️ Please enter a playlist URL")
    
    with st.spinner("🔍 Processing playlist..."):
        videos, playlist_title = process_playlist(playlist_url, start_index)
        
        if videos:
            st.success(f"✅ Successfully processed {len(videos)} videos from: {playlist_title}")
            
            # Display download links in a nice format
            for i, video in enumerate(videos, start_index):
                with st.expander(f"🎥 {i}. {video['title']}", expanded=True):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**Resolution:** {video['resolution']}")
                        if video['filesize']:
                            size_mb = video['filesize'] / (1024 * 1024)
                            st.markdown(f"**Size:** {size_mb:.1f} MB")
                        
                    with col2:
                        st.markdown(f"[Download Video 📥]({video['url']})")
            
            # Add helpful instructions
            st.info("""
            💡 **Download Tips:**
            - Right-click on 'Download Video' and select 'Save link as...' to choose filename
            - Videos will save to your default downloads folder
            - Some browsers might ask for download confirmation
            """)
        else:
            st.error("❌ No videos found. Please check the URL and try again.")
