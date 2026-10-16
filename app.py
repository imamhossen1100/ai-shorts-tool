import streamlit as st
import os
import json
import re
from youtube_transcript_api import YouTubeTranscriptApi
from google import genai
from google.genai import types

# Page Config
st.set_page_config(
    page_title="ClipCraft AI | SaaS Video Automation",
    page_icon="⚡",
    layout="wide"
)

# SaaS Custom CSS Styling for Stunning UI/UX
st.markdown("""
    <style>
    /* Main Theme & Background */
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    
    /* SaaS Hero Banner */
    .saas-hero {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
        padding: 2.5rem;
        border-radius: 16px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.4);
    }
    .saas-hero h1 {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    .saas-hero p {
        font-size: 1.1rem;
        opacity: 0.9;
    }

    /* Metric / Stats Card */
    .metric-container {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 1.2rem;
        border-radius: 12px;
        text-align: center;
        backdrop-filter: blur(10px);
    }

    /* Clip Output Card */
    .clip-card {
        background: #1e293b;
        border: 1px solid #334155;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.2rem;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .clip-card:hover {
        border-color: #6366f1;
        transform: translateY(-2px);
    }

    /* Buttons Styling */
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        border-radius: 8px;
        width: 100%;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%);
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# SaaS Header Banner
st.markdown("""
    <div class="saas-hero">
        <h1>⚡ ClipCraft AI Studio</h1>
        <p>Transform long-form YouTube videos into viral TikToks, Reels & Shorts using next-gen AI.</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar SaaS Navigation & Controls
with st.sidebar:
    st.image("https://img.icons8.com/clouds/100/video-trimming.png", width=80)
    st.markdown("### 🛠️ Workspace Control")
    
    api_key = st.text_input("🔑 Gemini API Key:", type="password", help="Enter your free Google AI Studio API key.")
    
    st.markdown("---")
    st.markdown("### ⚙️ AI Generation Config")
    num_clips = st.slider("Target Clips Count", min_value=2, max_value=6, value=4)
    target_platform = st.selectbox("Platform Format", ["TikTok / Reels / Shorts (9:16)", "YouTube Standard (16:9)"])
    
    st.markdown("---")
    st.info("💡 **SaaS Status:** System operational. Zero monthly fees. 100% Open Source.")

# Helper Function: Extract YouTube Video ID
def extract_video_id(url):
    pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None

# Main Input Section inside a SaaS Card container
st.markdown("### 📥 Project Input")
col_input1, col_input2 = st.compat_loaders if hasattr(st, 'compat_loaders') else st.columns([4, 1])

with col_input1:
    video_url = st.text_input("YouTube Video URL", placeholder="https://www.youtube.com/watch?v=...", label_visibility="collapsed")

generate_btn = st.button("🚀 Analyze & Generate Viral Shorts")

if generate_btn:
    if not api_key:
        st.error("⚠️ Please enter your Gemini API Key in the sidebar to proceed.")
    elif not video_url:
        st.warning("⚠️ Please provide a valid YouTube video URL.")
    else:
        video_id = extract_video_id(video_url)
        if not video_id:
            st.error("❌ Invalid YouTube URL format. Please check and try again.")
        else:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("🔄 Connecting to YouTube Data Stream...")
            progress_bar.progress(25)
            
            try:
                # Fetch transcript
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['bn', 'en', 'hi'])
                
                full_transcript_text = ""
                for item in transcript_list:
                    start_time = int(item['start'])
                    duration = int(item['duration'])
                    text = item['text']
                    full_transcript_text += f"[{start_time}s - {start_time+duration}s]: {text}\n"

                status_text.text("🧠 AI Neural Engine analyzing hooks and viral patterns...")
                progress_bar.progress(60)

                # Gemini API Call
                client = genai.Client(api_key=api_key)
                
                prompt = f"""
                You are an elite AI growth hacker and viral video editor like OpusClip.
                Analyze the following video transcript with timestamps.
                Identify exactly {num_clips} most engaging, high-retention, viral-worthy segments suitable for {target_platform} (duration between 30 to 60 seconds each).

                Transcript:
                {full_transcript_text[:12000]}

                Respond ONLY with a valid JSON array in the following format (no markdown blocks around it, pure JSON):
                [
                  {{
                    "title": "Catchy Title for Short 1",
                    "start_time": 12,
                    "end_time": 55,
                    "hook": "Why this segment will go viral",
                    "viral_score": 95,
                    "suggested_caption": "Engaging caption with hashtags"
                  }}
                ]
                """

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        temperature=0.3
                    )
                )

                progress_bar.progress(90)
                status_text.text("✨ Rendering SaaS Dashboard Results...")
                
                results = json.loads(response.text)
                progress_bar.progress(100)
                status_text.empty()
                progress_bar.empty()

                st.success(f"🎉 Successfully extracted {len(results)} high-potential viral segments!")
                st.markdown("---")
                st.markdown("### 🔥 Generated Viral Shorts Dashboard")

                for idx, clip in enumerate(results, 1):
                    with st.container():
                        st.markdown(f"""
                        <div class="clip-card">
                            <h3>🎬 Clip #{idx}: {clip.get('title')}</h3>
                            <p style='color: #94a3b8; font-size: 0.9rem;'>⏱️ <b>Timestamp:</b> {clip.get('start_time')}s — {clip.get('end_time')}s &nbsp;|&nbsp; 📈 <b>Viral Score:</b> <span style='color: #22c55e; font-weight: bold;'>{clip.get('viral_score')}/100</span></p>
                            <p>💡 <b>Hook Analysis:</b> {clip.get('hook')}</p>
                            <hr style='border-color: #334155;'>
                            <p style='background: #0f172a; padding: 10px; border-radius: 6px;'>📝 <b>Caption & Tags:</b><br>{clip.get('suggested_caption')}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        col_link1, col_link2 = st.columns([1, 1])
                        with col_link1:
                            yt_time_link = f"https://www.youtube.com/watch?v={video_id}&t={clip.get('start_time')}s"
                            st.markdown(f"[🔗 Watch Segment on YouTube]({yt_time_link})")

            except Exception as e:
                progress_bar.empty()
                status_text.empty()
                st.error(f"❌ Error processing video: {str(e)}")