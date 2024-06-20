from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import speech_recognition as sr
from gtts import gTTS
import os

pro = Flask(__name__)
CORS(pro)

@pro.route('/')
def index():
    return render_template('index.html')

@pro.route('/speech_to_text', methods=['POST'])
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise, please wait...")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening... Please speak now.")
        audio = recognizer.listen(source)
        
        try:
            print("Recognizing...")
            text = recognizer.recognize_google(audio)
            print(f"Text: {text}")
            return jsonify({'text': text})
        except sr.RequestError as e:
            return jsonify({'error': f"Could not request results from Google Speech Recognition service; {e}"})
        except sr.UnknownValueError:
            return jsonify({'error': "Google Speech Recognition could not understand audio"})
        except Exception as e:
            return jsonify({'error': f"Error: {e}"})

@pro.route('/text_to_speech', methods=['POST'])
def text_to_speech():
    text = request.form.get('text')
    if not text:
        return jsonify({'error': 'No text provided'})
    try:
        tts = gTTS(text=text, lang='en')
        tts.save("static/output.mp3")
        return jsonify({'message': 'Text-to-speech conversion completed'})
    except Exception as e:
        return jsonify({'error': f"Error: {e}"})

if __name__ == "__main__":
    pro.run(debug=True)
