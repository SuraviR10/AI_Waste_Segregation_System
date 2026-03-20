import streamlit as st
import time
import base64
from pathlib import Path
import threading
import io
import html as _html
import re

def calculate_speech_duration(text):
    """
    Calculate approximate duration of spoken text in seconds.
    Accounts for multilingual speech rates and sentence complexity.
    Average speech rates:
    - English: 150 words per minute = 2.5 words per second
    - Hindi/Kannada: 120 words per minute = 2 words per second (slower, more syllables)
    """
    if not text:
        return 2.0
    
    # Remove emojis and HTML for accurate word count
    clean_text = re.sub(r'[^\w\s\u0600-\u06FF\u0900-\u097F]', '', text)
    word_count = len(clean_text.split())
    
    # Conservative calculation for multilingual support
    # Hindi and Kannada typically take 20-30% longer to speak
    duration = (word_count / 2.0) + 1.5  # 2 words per second + buffer
    
    # Minimum 2 seconds, maximum 30 seconds (safety cap)
    return max(2.0, min(duration, 30.0))

def generate_tts_bytes(text, language='en'):
    """Generate TTS audio bytes. Prefer gTTS (browser playback), fall back to None."""
    # Try Google Cloud Text-to-Speech (higher quality) when credentials available
    try:
        from google.cloud import texttospeech
        client = texttospeech.TextToSpeechClient()
        # Map simple codes to Google locale codes
        locale_map = {'en': 'en-US', 'hi': 'hi-IN', 'kn': 'kn-IN'}
        voice_lang = locale_map.get(language, language or 'en-US')
        synthesis_input = texttospeech.SynthesisInput(text=text or '')
        voice = texttospeech.VoiceSelectionParams(language_code=voice_lang, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
        response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
        return response.audio_content
    except Exception:
        pass

    # Fallback to gTTS (works without cloud credentials)
    try:
        from gtts import gTTS
        buf = io.BytesIO()
        # gTTS expects language short codes like 'hi', 'kn', 'en'
        gtts_lang = language if language in ('hi', 'kn', 'en') else 'en'
        tts = gTTS(text=text or '', lang=gtts_lang)
        tts.write_to_fp(buf)
        buf.seek(0)
        return buf.read()
    except Exception:
        return None


def _pyttsx3_speak(text, language='en'):
    """Fallback TTS using pyttsx3 in a background thread."""
    try:
        import pyttsx3
        engine = pyttsx3.init()
        voices = list(engine.getProperty('voices') or [])
        if language == 'hi':
            for voice in voices:
                try:
                    if 'hindi' in voice.name.lower() or 'hi-' in voice.id.lower():
                        engine.setProperty('voice', voice.id)
                        break
                except Exception:
                    continue
        elif language == 'kn':
            for voice in voices:
                try:
                    if 'kannada' in voice.name.lower() or 'kn-' in voice.id.lower():
                        engine.setProperty('voice', voice.id)
                        break
                except Exception:
                    continue

        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)
        engine.say(text or '')
        engine.runAndWait()
    except Exception:
        return

def get_image_base64(image_path):
    """Convert image to base64 for embedding"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

def show_talking_assistant(mood='happy', message='', duration=None, voice_enabled=True, language='en'):
    """Display animated talking Earth assistant with mouth movement and voice"""
    # Auto-calculate duration based on message length if not provided
    if duration is None:
        duration = calculate_speech_duration(message)
    
    # Prepare safe message for rendering
    message_safe = _html.escape(message or '')

    # Play audio in browser using gTTS if available, otherwise fallback to pyttsx3 in background
    audio_bytes = None
    if voice_enabled:
        audio_bytes = generate_tts_bytes(message or '', language)
        if audio_bytes:
            try:
                st.audio(audio_bytes, format='audio/mp3', autoplay=True)
            except Exception:
                # If streamlit audio fails, fallback to local pyttsx3
                t = threading.Thread(target=_pyttsx3_speak, args=(message or '', language))
                t.daemon = True
                t.start()
        else:
            t = threading.Thread(target=_pyttsx3_speak, args=(message or '', language))
            t.daemon = True
            t.start()
    
    # Map moods to image files
    mood_images = {
        'sad': 'earth_sad.jpg',
        'happy': 'earth_happy.jpg', 
        'thinking': 'earth_thinking.jpg'
    }
    
    # Get the appropriate image
    image_file = mood_images.get(mood, 'earth_happy.jpg')
    image_path = Path('images') / image_file
    
    # Convert image to base64
    img_base64 = get_image_base64(image_path)
    
    if img_base64:
        # Display with talking animation using components.html for proper rendering
        try:
            import streamlit.components.v1 as components
        except Exception:
            from streamlit import components as components

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <style>
        :root {{ --accent1: #34d399; --accent2: #60a5fa; --bg1: #f0f9ff; }}
        
        @keyframes popIn {{
            0% {{ transform: scale(0) translate(-50%, -50%); opacity: 0; }}
            50% {{ transform: scale(1.1) translate(-50%, -50%); }}
            100% {{ transform: scale(1) translate(-50%, -50%); opacity: 1; }}
        }}
        
        @keyframes popOut {{
            0% {{ transform: scale(1); opacity: 1; }}
            100% {{ transform: scale(0.5); opacity: 0; }}
        }}
        
        @keyframes talk {{
            0%, 100% {{ transform: scaleY(1); }}
            50% {{ transform: scaleY(0.95); }}
        }}
        
        @keyframes float {{
            0%, 100% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-15px); }}
        }}
        
        @keyframes slideIn {{ 
            from {{ transform: translateY(40px); opacity: 0; }} 
            to {{ transform: translateY(0); opacity: 1; }} 
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: scale(0.8); }}
            to {{ opacity: 1; transform: scale(1); }}
        }}
        
        @keyframes wave {{
            0%, 100% {{ height: 20px; }}
            50% {{ height: 40px; }}
        }}
        
        .assistant-container {{
            text-align: center;
            padding: 2rem;
            background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(200,230,201,0.3) 100%);
            border-radius: 35px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
            animation: popIn 0.3s cubic-bezier(0.36, 0, 0.66, 1) forwards;
            transform-origin: center;
            margin: 20px auto;
            max-width: 400px;
            opacity: 1;
        }}
        
        .earth-image {{
            width: 280px;
            height: 280px;
            border-radius: 50%;
            object-fit: cover;
            box-shadow: 0 30px 80px rgba(15, 23, 42, 0.2);
            animation: float 3s ease-in-out infinite;
            border: 8px solid rgba(255,255,255,0.9);
            transition: transform 0.4s ease;
        }}
        
        .sound-waves {{
            display: flex;
            justify-content: center;
            gap: 8px;
            margin-top: 1.5rem;
        }}
        
        .wave {{
            width: 5px;
            height: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
            animation: wave 0.6s ease-in-out infinite;
        }}
        
        .wave:nth-child(2) {{ animation-delay: 0.1s; }}
        .wave:nth-child(3) {{ animation-delay: 0.2s; }}
        .wave:nth-child(4) {{ animation-delay: 0.3s; }}
        .wave:nth-child(5) {{ animation-delay: 0.4s; }}
        
        .speech-bubble {{
            background: white;
            border-radius: 25px;
            padding: 2rem;
            margin-top: 2.5rem;
            box-shadow: 0 12px 40px rgba(0,0,0,0.1);
            position: relative;
            animation: slideIn 0.5s ease-out 0.1s backwards;
        }}
        
        .speech-bubble::before {{
            content: '';
            position: absolute;
            top: -20px;
            left: 50%;
            transform: translateX(-50%);
            width: 0;
            height: 0;
            border-left: 25px solid transparent;
            border-right: 25px solid transparent;
            border-bottom: 25px solid white;
        }}
        
        .speech-text {{
            font-size: 1.3rem;
            color: #0f172a;
            line-height: 1.7;
            margin: 0;
            font-weight: 600;
            letter-spacing: 0.3px;
        }}
        </style>
        </head>
        <body>
        <div class="assistant-container" id="container">
            <img src="data:image/jpeg;base64,{img_base64}" class="earth-image" alt="Earth" loading="lazy">
            <div class="sound-waves">
                <div class="wave"></div>
                <div class="wave"></div>
                <div class="wave"></div>
                <div class="wave"></div>
                <div class="wave"></div>
            </div>
            <div class="speech-bubble" role="status" aria-live="polite">
                <p class="speech-text">{message_safe}</p>
            </div>
        </div>
        <script>
            // Auto-hide after duration
            setTimeout(function() {{
                var container = document.getElementById('container');
                container.style.animation = 'popOut 0.4s ease-in forwards';
            }}, {int(duration * 1000) - 400});
        </script>
        </body>
        </html>
        """
        components.html(html_content, height=650)
    else:
        # Fallback to emoji version
        try:
            import streamlit.components.v1 as components
        except Exception:
            from streamlit import components as components

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <style>
        @keyframes popIn {{
            0% {{ transform: scale(0); opacity: 0; }}
            100% {{ transform: scale(1); opacity: 1; }}
        }}
        
        @keyframes popOut {{
            0% {{ transform: scale(1); opacity: 1; }}
            100% {{ transform: scale(0); opacity: 0; }}
        }}
        
        @keyframes float {{ 
            0%, 100% {{ transform: translateY(0px); }} 
            50% {{ transform: translateY(-15px); }} 
        }}
        
        .assistant-container {{ 
            text-align: center; 
            padding: 3rem; 
            background: linear-gradient(135deg, #e3f2fd 0%, #e8f5e9 100%); 
            border-radius: 35px;
            animation: popIn 0.3s ease-out forwards;
            margin: 20px auto;
            max-width: 400px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.1);
            opacity: 1;
        }}
        
        .earth-emoji {{ 
            font-size: 8rem; 
            animation: float 3s ease-in-out infinite;
            display: block;
        }}
        
        .speech-bubble {{ 
            background: white; 
            border-radius: 25px; 
            padding: 2rem; 
            margin-top: 2rem; 
            box-shadow: 0 12px 40px rgba(0,0,0,0.1);
            animation: slideIn 0.5s ease-out 0.1s backwards;
        }}
        
        .speech-text {{ 
            font-size: 1.4rem; 
            color: #2c3e50; 
            line-height: 1.7; 
            margin: 0; 
            font-weight: 600; 
        }}
        
        @keyframes slideIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        </style>
        </head>
        <body>
        <div class="assistant-container" id="container">
            <span class="earth-emoji">🌍</span>
            <div class="speech-bubble"><p class="speech-text">{message_safe}</p></div>
        </div>
        <script>
            setTimeout(function() {{
                var container = document.getElementById('container');
                container.style.animation = 'popOut 0.4s ease-in forwards';
            }}, {int(duration * 1000) - 400});
        </script>
        </body>
        </html>
        """
        components.html(html_content, height=550)
    
    # Wait for audio to complete (with small buffer)
    time.sleep(max(duration, 1.0))

def show_quick_reaction(mood='happy', text='', duration=2):
    """Show a quick animated reaction from Earth"""
    
    reactions = {
        'happy': '😊',
        'sad': '😢',
        'thinking': '🤔',
        'excited': '🤩',
        'worried': '😰'
    }
    
    emoji = reactions.get(mood, '🌍')
    
    st.markdown(f"""
    <style>
    @keyframes popIn {{
        0% {{ transform: scale(0); opacity: 0; }}
        50% {{ transform: scale(1.2); }}
        100% {{ transform: scale(1); opacity: 1; }}
    }}
    
    @keyframes shake {{
        0%, 100% {{ transform: rotate(0deg); }}
        25% {{ transform: rotate(-10deg); }}
        75% {{ transform: rotate(10deg); }}
    }}
    
    .quick-reaction {{
        text-align: center;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        margin: 0.5rem 0;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        animation: popIn 0.5s ease-out;
    }}
    
    .reaction-emoji {{
        font-size: 4rem;
        animation: shake 0.5s ease-in-out;
    }}
    
    .reaction-text {{
        font-size: 1.1rem;
        color: #2c3e50;
        margin-top: 0.5rem;
        font-weight: 600;
    }}
    </style>
    
    <div class="quick-reaction">
        <div class="reaction-emoji">{emoji}🌍</div>
        <div class="reaction-text">{text}</div>
    </div>
    """, unsafe_allow_html=True)
    
    time.sleep(duration)
