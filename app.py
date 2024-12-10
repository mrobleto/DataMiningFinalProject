# Import necessary libraries
import streamlit as st
import os
from together import Together

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
            model="together/TravelExpertModel",  # Change to a model that can handle travel queries
            messages=[{"role": "user", "content": prompt}]
        )

        # Extract the answer from the response
        travel_answer = response.choices[0].message.content.strip()
        return travel_answer

    except Exception as e:
        return f"Error with Together AI: {e}"


# Streamlit app layout
st.title("Travel Expert: Ask Your Travel Questions!")
st.write("Enter your travel-related question, and I will provide an answer.")

# Input box for the user to enter a travel question or description
description = st.text_area("Your Travel Question or Description", placeholder="Describe your travel question or request")

# Button to trigger travel query processing
if st.button("Get Travel Answer"):
    if description.strip():
        st.write("### Travel Answer")
        # Get the travel-related answer
        travel_answer = answer_travel_question(description)
        st.write(travel_answer)
    else:
        st.error("Please provide a valid travel-related description or question.")
