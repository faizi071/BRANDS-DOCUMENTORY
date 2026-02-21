import streamlit as st
import requests
from datetime import datetime, timedelta

# Direct API Key
API_KEY = "AIzaSyAPdhFhTpgu-Fuftl4WuZ9CW1a3rC4tRKI"

YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"
YOUTUBE_CHANNEL_URL = "https://www.googleapis.com/youtube/v3/channels"

st.title("YouTube Viral Topics Tool")

days = st.number_input("Enter Days to Search (1-30):", min_value=1, max_value=30, value=5)

keywords = [
    "brand turnaround",
    "corporate turnaround strategy",
    "business case study",
    "brand repositioning",
    "rebranding strategy",
    "marketing controversy",
    "revenue collapse analysis",
    "demand vs supply shock",
    "luxury brand strategy",
    "product-market fit",
    "brand heritage strategy",
    "consumer trust",
    "brand backlash",
    "price sensitivity",
    "subscription business model",
    "business documentary",
    "brand failure",
    "viral marketing fail",
    "brand strategy",
    "marketing case study",
    "business failure",
    "marketing analysis",
    "Jaguar Land Rover",
    "brand collapse"
]

if st.button("Fetch Data"):
    try:
        start_date = (datetime.utcnow() - timedelta(days=int(days))).isoformat("T") + "Z"
        all_results = []

        for keyword in keywords:
            st.write(f"Searching for keyword: {keyword}")

            search_params = {
                "part": "snippet",
                "q": keyword,
                "type": "video",
                "order": "viewCount",
                "publishedAfter": start_date,
                "maxResults": 5,
                "key": API_KEY,
            }

            response = requests.get(YOUTUBE_SEARCH_URL, params=search_params)
            data = response.json()

            if "items" not in data or not data["items"]:
                continue

            videos = data["items"]

            video_ids = [video["id"]["videoId"] for video in videos if "videoId" in video["id"]]
            channel_ids = [video["snippet"]["channelId"] for video in videos]

            stats_params = {
                "part": "statistics",
                "id": ",".join(video_ids),
                "key": API_KEY
            }

            stats_response = requests.get(YOUTUBE_VIDEO_URL, params=stats_params)
            stats_data = stats_response.json()

            channel_params = {
                "part": "statistics",
                "id": ",".join(channel_ids),
                "key": API_KEY
            }

            channel_response = requests.get(YOUTUBE_CHANNEL_URL, params=channel_params)
            channel_data = channel_response.json()

            if "items" not in stats_data or "items" not in channel_data:
                continue

            stats = stats_data["items"]
            channels = channel_data["items"]

            for video, stat, channel in zip(videos, stats, channels):
                title = video["snippet"].get("title", "N/A")
                description = video["snippet"].get("description", "")[:200]
                video_url = f"https://www.youtube.com/watch?v={video['id']['videoId']}"
                views = int(stat["statistics"].get("viewCount", 0))
                subs = int(channel["statistics"].get("subscriberCount", 0))

                if subs < 3000:
                    all_results.append({
                        "Title": title,
                        "Description": description,
                        "URL": video_url,
                        "Views": views,
                        "Subscribers": subs
                    })

        if all_results:
            st.success(f"Found {len(all_results)} results!")
            for result in all_results:
                st.markdown(f"""
                **Title:** {result['Title']}  
                **Description:** {result['Description']}  
                **URL:** [Watch Video]({result['URL']})  
                **Views:** {result['Views']}  
                **Subscribers:** {result['Subscribers']}
                """)
                st.write("---")
        else:
            st.warning("No results found.")

    except Exception as e:
        st.error(f"An error occurred: {e}")
