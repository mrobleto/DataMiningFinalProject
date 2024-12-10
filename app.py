import streamlit as st
from PyPDF2 import PdfReader
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline

# Configure Hugging Face Summarization and Q&A Pipelines
summarizer = pipeline("summarization", model="google/flan-t5-large")
qa_pipeline = pipeline("question-answering", model="google/flan-t5-large")

# Function to extract text from PDFs
def extract_text_from_pdfs(uploaded_files):
    content = ""
    for uploaded_file in uploaded_files:
        pdf_reader = PdfReader(uploaded_file)
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
st.sidebar.header("Upload PDF Travel Guides")
uploaded_files = st.sidebar.file_uploader("Upload PDF travel guides", accept_multiple_files=True)

# Input YouTube video URLs
st.sidebar.header("YouTube Videos")
user_video_urls = st.sidebar.text_area("Enter YouTube URLs (one per line)").splitlines()

# Combine all content (uploaded PDFs and YouTube transcripts)
combined_content = ""

# Extract content from user-uploaded PDFs
if uploaded_files:
    uploaded_pdf_content = extract_text_from_pdfs(uploaded_files)
    combined_content += uploaded_pdf_content

# Extract content from YouTube videos if URLs are provided
if user_video_urls:
    youtube_content = extract_youtube_transcript(user_video_urls)
    combined_content += youtube_content

# Query Box for the user to ask a question
query = st.text_input("Ask a question about your Europe trip:")

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
