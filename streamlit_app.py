import streamlit as st
import requests
import openai
from news_api import NewsAPI
from news_video import VideoGenerator
from dotenv import load_dotenv
import os

load_dotenv()

news_api_key = os.getenv('NEWS_API_KEY')
# Create an instance of the News Retreiver class
news_client = NewsAPI(api_key=news_api_key)
video_api_key = os.getenv("BEARER_TOKEN")
# Create an instance of the VideoGenerator class
video_generator = VideoGenerator(video_api_key)


st.set_page_config(
    page_title="AI News Anchor",
    layout="wide"
)

# Set app title
st.title("AI News Anchor")
st.markdown('<style>h1{color: orange; text-align: center;}</style>', unsafe_allow_html=True)
st.subheader('Built with Midjourney, OpenAI, D-ID, Streamlit and ❤️')
st.markdown('<style>h3{color: pink;  text-align: center;}</style>', unsafe_allow_html=True)


# Input for image URL
image_url = st.text_input("Enter Image URL", "")

# Input for query keywords
query = st.text_input("Enter Query Keywords", "")

# Slider for selecting the number of news
num_news = st.slider("Number of News", min_value=1, max_value=5, value=3)

# Button to generate video
if st.button("Generate"):
    if image_url.strip() and query.strip() and num_news is not None and num_news > 0:
        col1, col2, col3 = st.columns([1,1,1])
        # Process the image (you can add your image processing code here)
        with col1:
            st.info("Your AI News Anchor: Sophie")
            st.image(image_url, caption="Anchor Image", use_column_width=True)
        #to get a list of descriptions

        with col2:
            desc_list = news_client.get_news_descriptions(query, num_news=num_news)
            st.success("Your Fetched News")
            st.write(desc_list)
            
            #to get a concatenated string of descriptions
            # desc_string = news_client.get_news_string(query, num_news=num_news)
            numbered_paragraphs = "\n".join([f"{i+1}. {paragraph}" for i, paragraph in enumerate(desc_list)])
            st.write(numbered_paragraphs)


        with col3:
            final_text = f"""
                Hello World, I'm Sophie, your AI News Anchor. Bringing you the latest updates for {query}.
                Here are the news for you: {numbered_paragraphs}
                That's all for today. Stay tuned for more news, Thank you!
            """

            video_url = video_generator.generate_video(final_text, image_url)

            st.warning("AI News Anchor Video")
            # Display the video
            st.video(video_url)
    
    else:
        st.write("Failed to fetch news data. Please check your query and API key.")
