import streamlit as st
import os
from together import Together
from PyPDF2 import PdfReader
import requests
from youtube_transcript_api import YouTubeTranscriptApi

# Set up the API key for Together
os.environ['TOGETHER_API_KEY'] = st.secrets["TOGETHER_API_KEY"]

# Initialize Together client
client = Together()

# Function to answer travel-related questions
def answer_travel_question(description):
    """
    Answer a travel-related question based on a natural language description.

    Parameters:
    description (str): A plain-text description or question about travel.

    Returns:
    str: Answer to the travel-related question or an error message.
    """
    try:
        prompt = (
            f"You are a travel expert. Based on the following description or question, "
            f"provide a detailed and informative answer about travel.\n\n"
            f"Description/Question: {description}\n\n"
            f"Answer:"
        )

        # Call Together AI to generate a response based on the travel question
        response = client.chat.completions.create(
            model="codellama/CodeLlama-34b-Instruct-hf",  # Change to a model that can handle travel queries
            messages=[{"role": "user", "content": prompt}]
        )

        # Extract the answer from the response
        travel_answer = response.choices[0].message.content.strip()
        return travel_answer

    except Exception as e:
        return f"Error with Together AI: {e}"

# Function to summarize text from PDF
def summarize_pdf(uploaded_file):
    """
    Summarize the content of the uploaded PDF file.
    
    Parameters:
    uploaded_file (UploadedFile): The PDF file uploaded by the user.
    
    Returns:
    str: The summarized content from the PDF file.
    """
    try:
        # Read the PDF
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        
        # Generate summary using Together API
        prompt = f"Summarize the following text:\n\n{text}\n\nSummary:"
        
        response = client.chat.completions.create(
            model="codellama/CodeLlama-34b-Instruct-hf",  # Change to a model that handles summarization
            messages=[{"role": "user", "content": prompt}]
        )

        summary = response.choices[0].message.content.strip()
        return summary

    except Exception as e:
        return f"Error with PDF processing: {e}"

# Function to summarize YouTube video based on its transcript
def summarize_youtube_link(link):
    """
    Summarize the transcript of a YouTube video given its URL.
    
    Parameters:
    link (str): The URL of the YouTube video.
    
    Returns:
    str: The summarized content of the YouTube video.
    """
    try:
        # Extract video ID from YouTube URL
        video_id = link.split("v=")[-1]
        
        # Get transcript of the YouTube video
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([entry['text'] for entry in transcript])
        
        # Generate summary using Together API
        prompt = f"Summarize the following YouTube transcript:\n\n{transcript_text}\n\nSummary:"
        
        response = client.chat.completions.create(
            model="codellama/CodeLlama-34b-Instruct-hf",  # Change to a model that handles summarization
            messages=[{"role": "user", "content": prompt}]
        )

        summary = response.choices[0].message.content.strip()
        return summary

    except Exception as e:
        return f"Error with YouTube processing: {e}"

# Streamlit app layout
st.image("https://github.com/mrobleto/DataMiningFinalProject/raw/main/stockpic.jpg", width=250) # Add your logo URL here
st.title("Ursula's & Marisabel's Your Travel Experts: All You Need to Know!")
st.write("Enter your travel-related question, upload a PDF for summarization, or provide a YouTube link for summarization.")

# Input box for the user to enter a travel question or description
description = st.text_area("Your Travel Question or Description and click 'Get Travel Answer' below", placeholder="Describe your travel question or request")

# Button to trigger travel query processing
if st.button("Get Travel Answer"):
    if description.strip():
        st.write("### Travel Answer")
        # Get the travel-related answer
        travel_answer = answer_travel_question(description)
        st.write(travel_answer)
    else:
        st.error("Please provide a valid travel-related description or question.")

# PDF file upload section
uploaded_pdf = st.file_uploader("Upload a PDF for summarization", type="pdf")

if uploaded_pdf:
    st.write("### PDF Summary")
    summary_pdf = summarize_pdf(uploaded_pdf)
    st.write(summary_pdf)

# YouTube link input section
youtube_link = st.text_input("Enter YouTube link to summarize")

if youtube_link:
    st.write("### YouTube Video Summary")
    summary_youtube = summarize_youtube_link(youtube_link)
    st.write(summary_youtube)
