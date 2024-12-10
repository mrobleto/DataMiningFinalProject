
import streamlit as st
from PyPDF2 import PdfReader
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline

# Configure Hugging Face Summarization and Q&A Pipelines
summarizer = pipeline("summarization", model="google/flan-t5-large")
qa_pipeline = pipeline("question-answering", model="google/flan-t5-large")

# Predefined YouTube videos
DEFAULT_VIDEO_URLS = [
    "https://www.youtube.com/watch?v=pfdb6u4HDoQ",
    "https://www.youtube.com/watch?v=7lvXbfNBIQg"
]

# Path to the predefined PDF
DEFAULT_PDF_PATH = "/content/swiss1.pdf"

# Function to extract text from PDFs
def extract_text_from_pdfs(uploaded_files):
    content = ""
    for uploaded_file in uploaded_files:
        pdf_reader = PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            content += page.extract_text()
    return content

# Function to extract text from a single predefined PDF
def extract_text_from_default_pdf():
    content = ""
    with open(DEFAULT_PDF_PATH, "rb") as default_pdf:
        pdf_reader = PdfReader(default_pdf)
        for page in pdf_reader.pages:
            content += page.extract_text()
    return content

# Function to extract captions from YouTube videos
def extract_youtube_transcript(video_urls):
    content = ""
    for video_url in video_urls:
        video_id = video_url.split("v=")[-1]
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            content += " ".join([entry["text"] for entry in transcript])
        except Exception as e:
            st.error(f"Error fetching transcript for {video_url}: {e}")
    return content

# Summarize content using Hugging Face
def summarize_content(content):
    return summarizer(content, max_length=512, min_length=50, truncation=True)[0]["summary_text"]

# Answer questions using Hugging Face
def answer_query(content, query):
    return qa_pipeline({"context": content, "question": query})["answer"]

# Streamlit App
st.title("Europe Travel Itinerary Guide with Hugging Face Transformers")

# Upload PDFs
st.sidebar.header("Upload Additional Files")
uploaded_files = st.sidebar.file_uploader("Upload PDF travel guides", accept_multiple_files=True)

# Input YouTube video URLs
st.sidebar.header("YouTube Videos")
user_video_urls = st.sidebar.text_area("Enter YouTube URLs (one per line)").splitlines()

# Add default videos to the list of URLs
video_urls = DEFAULT_VIDEO_URLS + user_video_urls

# Query Box
query = st.text_input("Ask a question about your Europe trip:")

# Extract content from default and user-uploaded PDFs
default_pdf_content = extract_text_from_default_pdf()
uploaded_pdf_content = extract_text_from_pdfs(uploaded_files) if uploaded_files else ""

# Extract content from YouTube videos
youtube_content = extract_youtube_transcript(video_urls) if video_urls else ""

# Combine all content
combined_content = default_pdf_content + uploaded_pdf_content + youtube_content

# Summarize content
if combined_content:
    with st.spinner("Summarizing key points from the content..."):
        summary = summarize_content(combined_content)
        st.subheader("Key Points Summary")
        st.write(summary)

# Respond to user queries
if query and combined_content:
    with st.spinner("Generating your travel guide..."):
        response = answer_query(combined_content, query)
        st.subheader("Travel Advice")
        st.write(response)
