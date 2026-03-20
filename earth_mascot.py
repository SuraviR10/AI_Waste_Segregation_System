import streamlit as st
import numpy as np
from earth_dialogues import EARTH_DIALOGUES

def show_earth_mascot(mood='thinking', message='', animate=True):
    earth_faces = {
        'thinking': '🤔🌍',
        'happy': '😊🌍',
        'sad': '😢🌍',
        'welcome': '👋🌍'
    }
    
    earth_icon = earth_faces.get(mood, '🌍')
    animation_style = ''
    
    if animate:
        if mood == 'thinking':
            animation_style = 'animation: bounce 1s infinite;'
        elif mood == 'happy':
            animation_style = 'animation: celebrate 0.8s ease-in-out infinite;'
        elif mood == 'sad':
            animation_style = 'animation: shake 0.5s ease-in-out;'
    
    st.markdown(f"""
    <style>
    @keyframes bounce {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-15px); }}
    }}
    @keyframes celebrate {{
        0%, 100% {{ transform: scale(1) rotate(0deg); }}
        25% {{ transform: scale(1.1) rotate(-5deg); }}
        75% {{ transform: scale(1.1) rotate(5deg); }}
    }}
    @keyframes shake {{
        0%, 100% {{ transform: translateX(0); }}
        25% {{ transform: translateX(-10px); }}
        75% {{ transform: translateX(10px); }}
    }}
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: scale(0.8); }}
        to {{ opacity: 1; transform: scale(1); }}
    }}
    </style>
    
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #e3f2fd 0%, #e8f5e9 100%);
                border-radius: 25px; margin: 1rem 0; box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                animation: fadeIn 0.5s ease-out;">
        <div style="font-size: 8rem; {animation_style}">{earth_icon}</div>
        <div style="background: white; border-radius: 20px; padding: 1.5rem; margin-top: 1rem;
                    box-shadow: 0 5px 15px rgba(0,0,0,0.1); position: relative;">
            <div style="position: absolute; top: -10px; left: 50%; transform: translateX(-50%);
                        width: 0; height: 0; border-left: 15px solid transparent;
                        border-right: 15px solid transparent; border-bottom: 15px solid white;"></div>
            <p style="font-size: 1.3rem; color: #2c3e50; margin: 0; line-height: 1.6;">{message}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def get_earth_message(context, waste_type=None, user_name=None):
    if context == 'welcome':
        return np.random.choice(EARTH_DIALOGUES['welcome'])
    elif context == 'thinking':
        return np.random.choice(EARTH_DIALOGUES['thinking'])
    elif context == 'correct':
        return np.random.choice(EARTH_DIALOGUES['correct'])
    elif context == 'wrong':
        return np.random.choice(EARTH_DIALOGUES['wrong'])
    elif context == 'impact' and waste_type:
        return np.random.choice(EARTH_DIALOGUES['impact'][waste_type])
    elif context == 'emotional':
        return np.random.choice(EARTH_DIALOGUES['emotional'])
    elif context == 'celebration':
        return np.random.choice(EARTH_DIALOGUES['celebration'])
    elif context == 'personalized' and user_name:
        return EARTH_DIALOGUES['personalized'].format(name=user_name)
    elif context == 'daily_tip':
        return np.random.choice(EARTH_DIALOGUES['daily_tips'])
    return ""
