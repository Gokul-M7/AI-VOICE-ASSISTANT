import openai
import speech_recognition as sr
from gtts import gTTS
import os
import playsound  

# OpenAI API Key
OPENAI_API_KEY = "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"  
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def speak(text):
    """Convert text to speech and play the audio using gTTS."""
    tts = gTTS(text)
    tts.save("response.mp3")
    
    # Use playsound to play audio on Windows
    playsound.playsound("response.mp3")

def listen():
    """Listen for voice input and return the recognized text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your question...")
        audio = recognizer.listen(source)
        
    try:
        # Recognize the speech using Google's Speech Recognition API
        print("Recognizing...")
        query = recognizer.recognize_google(audio)
        print(f"You said: {query}")
        return query
    except sr.UnknownValueError:
        speak("Sorry, I could not understand your speech. Could you please repeat?")
        return None
    except sr.RequestError:
        speak("Sorry, I couldn't reach the speech recognition service.")
        return None

def get_gpt_response(query):
    """Get a response from OpenAI's GPT model using the latest API format."""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # You can use "gpt-4" if needed
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": query},
            ],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    while True:
        # Get the voice input from the user
        query = listen()
        
        if query:
            # Get the response from OpenAI's GPT
            response = get_gpt_response(query)
            print(f"GPT-3 says: {response}")
            
            # Speak out the response
            speak(response)

if _name_ == "_main_":
    main()
