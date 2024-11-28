import streamlit as st
from gtts import gTTS
from io import BytesIO

# Function to convert text to speech using gTTS
def text_to_speech(text):
    try:
        # Convert text to speech using Google Text-to-Speech (gTTS)
        tts = gTTS(text)
        
        # Save speech to a BytesIO buffer
        audio_buffer = BytesIO()
        tts.save(audio_buffer)  # Save speech to the buffer
        audio_buffer.seek(0)  # Ensure the buffer is at the start
        return audio_buffer
    except Exception as e:
        st.write(f"Error during text-to-speech conversion: {e}")
        return None

# Check if we are running in Google Colab or Streamlit
def is_google_colab():
    try:
        # If running in Google Colab, this will be available
        import google.colab
        return True
    except ImportError:
        return False

# Streamlit app interface
st.title("Text-to-Speech Converter")
st.write("This app converts your text input into speech.")

# Prompt the user for text input
user_input = st.text_input("Enter some text to convert to speech:")

# If the user has entered text
if user_input:
    # Convert input text to speech
    audio_output = text_to_speech(user_input)

    # If audio was generated
    if audio_output:
        if is_google_colab():
            # Display in Google Colab (using IPython display)
            from IPython.display import Audio
            audio_output.seek(0)  # Rewind buffer to start
            st.write("Playing the generated audio response (Google Colab):")
            Audio(audio_output.read(), autoplay=True)
        else:
            # Save the in-memory audio to a temporary file for Streamlit
            with open("/tmp/temp_audio.mp3", "wb") as f:
                f.write(audio_output.read())  # Write audio buffer to temporary file

            # Stream the audio file in Streamlit
            st.write("Playing the generated audio response (Streamlit):")
            st.audio("/tmp/temp_audio.mp3", format="audio/mp3")
    else:
        st.write("Sorry, an error occurred while processing your request.")
