import streamlit as st
import requests
import collections

st.title("Speech to Text and Text to Speech")

# Speech to Text
st.header("Speech to Text")
if st.button("Start Listening"):
    response = requests.post("http://localhost:5000/speech_to_text")
    if response.status_code == 200:
        st.write(response.json().get('text'))
    else:
        st.write("Error: " + response.json().get('error'))

# Text to Speech
st.header("Text to Speech")
text = st.text_input("Enter text:")
if st.button("Convert to Speech"):
    response = requests.post("http://localhost:5000/text_to_speech", data={'text': text})
    if response.status_code == 200:
        st.write(response.json().get('message'))
        st.audio("http://localhost:5000/static/output.mp3")
    else:
        st.write("Error: " + response.json().get('error'))
