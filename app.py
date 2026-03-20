import streamlit as st
import cv2
import numpy as np
from PIL import Image
import pyttsx3
import pandas as pd
from datetime import datetime
import json
import os
from pathlib import Path
import base64
import time
from earth_dialogues import EARTH_DIALOGUES, EARTH_STORY, get_earth_message_multilang
from talking_assistant import show_talking_assistant, show_quick_reaction
from mistake_detection import (detect_wrong_bin_choice, show_mistake_penalty, 
                               show_environmental_damage_animation, show_real_time_guidance,
                               calculate_mistake_penalty, show_sad_earth_reaction)
import html as _html

# Try to import TensorFlow
try:
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    import tensorflow as tf
    from tensorflow import keras
    TF_AVAILABLE = True
except:
    TF_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="AI Waste Segregation System",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for pastel theme with animations
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Canva-inspired color palette */
    :root {
        /* Soft pastels */
        --pastel-mint: #C8E6C9;
        --pastel-blue: #B3E5FC;
        --pastel-pink: #F8BBD0;
        --pastel-yellow: #FFF9C4;
        --pastel-purple: #E1BEE7;
        --pastel-peach: #FFCCBC;
        --pastel-lavender: #EDE7F6;
        
        /* Vibrant accents (Canva-style) */
        --accent-purple: #7C3AED;
        --accent-pink: #EC4899;
        --accent-blue: #0EA5E9;
        --accent-green: #10B981;
        --accent-orange: #F97316;
        
        /* Neutrals */
        --white: #FFFFFF;
        --text-dark: #1F2937;
        --text-light: #6B7280;
        --bg-light: #F9FAFB;
    }
    
    * {
        font-family: 'Outfit', 'Inter', sans-serif;
    }
    
    /* Main container with soft gradient */
    .main {
        background: linear-gradient(135deg, #FAF5F0 0%, #EFF5FF 25%, #F5EFFF 50%, #EFF9F5 75%, #FFF5F8 100%);
        min-height: 100vh;
        padding: 20px;
    }
    
    /* Glassmorphism header - Canva style */
    .header-container {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.8);
        padding: 3.5rem 2rem;
        border-radius: 30px;
        text-align: center;
        margin-bottom: 2.5rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
        animation: floatIn 0.8s ease-out;
    }
    
    @keyframes floatIn {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .header-title {
        background: linear-gradient(135deg, #7C3AED 0%, #EC4899 50%, #0EA5E9 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 4rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -1px;
    }
    
    .header-subtitle {
        color: var(--text-light);
        font-size: 1.4rem;
        margin-top: 0.8rem;
        font-weight: 400;
        letter-spacing: 0.3px;
    }
    
    /* Realistic Dustbin Design - Canva Colors */
    .bin-card {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 25px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.12);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        margin: 15px;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.6);
        height: auto;
    }
    
    .bin-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, #7C3AED 0%, #EC4899 100%);
        opacity: 0;
        transition: opacity 0.4s ease;
        z-index: -1;
    }
    
    .bin-card:hover {
        transform: translateY(-12px);
        box-shadow: 0 24px 48px rgba(0, 0, 0, 0.15);
    }
    
    /* Dustbin body */
    .bin-body {
        position: relative;
        padding: 20px 10px;
    }
    
    /* Dustbin lid */
    .bin-lid {
        position: relative;
        margin-bottom: 15px;
        z-index: 10;
    }
    
    .bin-lid::before {
        content: '♻️';
        font-size: 3.5rem;
        display: block;
        margin-bottom: 10px;
    }
    
    /* Wheels */
    .bin-wheels {
        display: none;
    }
    
    .wheel {
        display: none;
    }
    
    .bin-card.active {
        animation: binShake 0.6s ease-in-out;
        box-shadow: 0 0 50px rgba(124, 58, 237, 0.5);
    }
    
    .bin-card.active .bin-lid {
        animation: lidBounce 0.6s ease-in-out;
    }
    
    @keyframes lidBounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    @keyframes binShake {
        0%, 100% { transform: rotate(0deg); }
        25% { transform: rotate(-2deg); }
        75% { transform: rotate(2deg); }
    }
    
    .bin-icon {
        font-size: 4.5rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .bin-label {
        font-size: 1.4rem;
        font-weight: 600;
        margin: 1rem 0 0.5rem 0;
        color: var(--text-dark);
        letter-spacing: 0.3px;
    }
    
    .bin-count {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #7C3AED 0%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Glassmorphism stats cards - Canva style */
    .stat-card {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.7);
        border-radius: 25px;
        padding: 2.5rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.09);
        margin: 12px;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        animation: fadeInUp 0.6s ease-out;
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .stat-card:hover {
        transform: translateY(-15px);
        box-shadow: 0 24px 48px rgba(0, 0, 0, 0.12);
        background: rgba(255, 255, 255, 0.75);
    }
    
    .stat-value {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #7C3AED 0%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0.8rem 0;
    }
    
    .stat-label {
        font-size: 1.1rem;
        color: var(--text-light);
        font-weight: 500;
        letter-spacing: 0.2px;
    }
    
    /* Animated badges - Canva style */
    .badge {
        display: inline-block;
        padding: 0.9rem 2rem;
        border-radius: 30px;
        font-weight: 600;
        margin: 0.7rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
        transition: all 0.3s ease;
        font-size: 1rem;
        letter-spacing: 0.3px;
    }
    
    .badge:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.16);
    }
    
    .badge-gold {
        background: linear-gradient(135deg, #FCD34D 0%, #FBBF24 100%);
        color: white;
        box-shadow: 0 8px 24px rgba(252, 211, 77, 0.3);
    }
    
    .badge-silver {
        background: linear-gradient(135deg, #E5E7EB 0%, #F3F4F6 100%);
        color: var(--text-dark);
        box-shadow: 0 8px 24px rgba(229, 231, 235, 0.3);
    }
    
    .badge-bronze {
        background: linear-gradient(135deg, #FB923C 0%, #F97316 100%);
        color: white;
        box-shadow: 0 8px 24px rgba(249, 115, 22, 0.3);
    }
    
    /* Detection result with 3D effect - Canva style */
    .detection-result {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(15px);
        border-radius: 30px;
        padding: 3rem 2.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.6);
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .confidence-bar {
        height: 40px;
        border-radius: 25px;
        background: linear-gradient(90deg, #C8E6C9 0%, #B3E5FC 50%, #E1BEE7 100%);
        transition: width 1s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
        overflow: hidden;
    }
    
    /* Fact box with gradient - Canva style */
    .fact-box {
        background: linear-gradient(135deg, #F8BBD0 0%, #FFCCBC 50%, #FFE0B2 100%);
        color: #FFFFFF;
        padding: 2.5rem;
        border-radius: 30px;
        margin: 1.5rem 0;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
        animation: fadeIn 0.8s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    .fact-title {
        font-size: 1.9rem;
        font-weight: 700;
        margin-bottom: 1.2rem;
        letter-spacing: 0.3px;
    }
    
    /* History items - Canva style */
    .history-item {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(15px);
        padding: 1.8rem;
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 0 8px 28px rgba(0, 0, 0, 0.1);
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        border-left: 5px solid;
        border-image: linear-gradient(135deg, #7C3AED, #EC4899) 1;
    }
    
    .history-item:hover {
        transform: translateX(12px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
        background: rgba(255, 255, 255, 0.95);
    }
    
    /* Buttons with 3D effect - Canva style */
    .stButton>button {
        background: linear-gradient(135deg, #7C3AED 0%, #EC4899 100%);
        color: white;
        border: none;
        border-radius: 35px;
        padding: 1.1rem 2.8rem;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 10px 32px rgba(124, 58, 237, 0.3);
        letter-spacing: 0.3px;
    }
    
    .stButton>button:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 50px rgba(124, 58, 237, 0.4);
    }
    
    .stButton>button:active {
        transform: translateY(-2px);
    }

    /* Navigation buttons in sidebar - Purple theme */
    section[data-testid="stSidebar"] .stButton>button {
        background: linear-gradient(135deg, #7C3AED 0%, #EC4899 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        margin-bottom: 0.5rem !important;
        font-weight: 600 !important;
        padding: 0.75rem 1.5rem !important;
    }

    section[data-testid="stSidebar"] .stButton>button:hover {
        box-shadow: 0 12px 32px rgba(124, 58, 237, 0.35) !important;
        transform: translateY(-3px) !important;
    }
    
    /* AI Chat bubble - Canva style */
    .ai-chat {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(15px);
        border-radius: 25px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 10px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.6);
        border-left: 6px solid #7C3AED;
        animation: slideInRight 0.5s ease-out;
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    /* Loading animation */
    .loading-spinner {
        border: 4px solid rgba(168, 216, 234, 0.3);
        border-top: 4px solid var(--pastel-blue);
        border-radius: 50%;
        width: 50px;
        height: 50px;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Footer - Canva style */
    .footer {
        text-align: center;
        padding: 2.5rem;
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(15px);
        color: var(--text-light);
        border-radius: 30px;
        margin-top: 3rem;
        border: 1px solid rgba(255, 255, 255, 0.6);
        font-size: 1.1rem;
        font-weight: 500;
        letter-spacing: 0.2px;
    }
    
    /* Sidebar styling - Canva style */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FAF5F0 0%, #EFF5FF 50%, #F5EFFF 100%);
    }
    
    /* Video container with 3D effect - Canva style */
    .video-container {
        border-radius: 30px;
        overflow: hidden;
        box-shadow: 0 16px 48px rgba(0, 0, 0, 0.15);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .video-container:hover {
        transform: scale(1.03);
        box-shadow: 0 24px 64px rgba(0, 0, 0, 0.18);
    }
    .nav-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: var(--text-dark);
        margin: 1rem 0 0.5rem 0;
        padding-left: 8px;
        letter-spacing: 0.6px;
        background: linear-gradient(135deg, #7C3AED 0%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .nav-link {
        display: block;
        padding: 0.8rem 1.2rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        background: rgba(255, 255, 255, 0.5);
        font-weight: 500;
    }
    .nav-link:hover { 
        transform: translateX(8px); 
        background: rgba(255, 255, 255, 0.8);
        box-shadow: 0 10px 28px rgba(0,0,0,0.1);
    }
    /* Content panel animations */
    .content-panel {
        animation: slideUp 0.4s ease-out;
    }
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    /* Improved card layout - Canva style */
    .main-card {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(15px);
        border-radius: 30px;
        padding: 2.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.7);
        transition: all 0.4s ease;
    }
    
    .main-card:hover {
        background: rgba(255, 255, 255, 0.9);
        box-shadow: 0 16px 48px rgba(0, 0, 0, 0.12);
    }
    /* Hide raw code/pre blocks by default to avoid leaking source on the page */
    pre, code {
        display: none !important;
    }
    /* Allow showing code when developer mode toggles a container with class show-code */
    .show-code pre, .show-code code {
        display: block !important;
        white-space: pre-wrap;
        background: rgba(10,10,10,0.85);
        color: #e6eef8;
        padding: 1rem;
        border-radius: 8px;
        overflow: auto;
        font-family: 'Courier New', monospace;
    }
    /* Slide-in right panel */
    .slide-panel {
        position: relative;
        transform: translateX(30px);
        opacity: 0;
        transition: transform 0.45s ease, opacity 0.45s ease;
    }
    .slide-panel.visible {
        transform: translateX(0px);
        opacity: 1;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if 'waste_counts' not in st.session_state:
        st.session_state.waste_counts = {'Plastic': 0, 'Paper': 0, 'Metal': 0, 'Organic': 0}
    if 'total_scans' not in st.session_state:
        st.session_state.total_scans = 0
    if 'points' not in st.session_state:
        st.session_state.points = 0
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'active_bin' not in st.session_state:
        st.session_state.active_bin = None
    if 'last_confidence' not in st.session_state:
        st.session_state.last_confidence = 0.0
    if 'selected_bin_info' not in st.session_state:
        st.session_state.selected_bin_info = None
    if 'sorting_animation' not in st.session_state:
        st.session_state.sorting_animation = False
    if 'manual_selection_mode' not in st.session_state:
        st.session_state.manual_selection_mode = False
    if 'pending_image' not in st.session_state:
        st.session_state.pending_image = None
    if 'daily_stats' not in st.session_state:
        st.session_state.daily_stats = {}
    if 'weekly_stats' not in st.session_state:
        st.session_state.weekly_stats = []
    if 'earth_mood' not in st.session_state:
        st.session_state.earth_mood = 'thinking'
    if 'show_earth' not in st.session_state:
        st.session_state.show_earth = True
    if 'user_name' not in st.session_state:
        st.session_state.user_name = None
    if 'developer_mode' not in st.session_state:
        st.session_state.developer_mode = False
    if 'correct_streak' not in st.session_state:
        st.session_state.correct_streak = 0


def show_slide_panel(title, content_html, height=320):
    """Render a slide-in panel with provided HTML content."""
    try:
        import streamlit.components.v1 as components
    except Exception:
        from streamlit import components as components

    safe_title = _html.escape(title or '')
    panel_html = f"""
    <div class="slide-panel visible">
        <div class="stat-card">
            <h3 style="margin-top:0">{safe_title}</h3>
            {content_html}
        </div>
    </div>
    """
    components.html(panel_html, height=height)

# Waste classification model with TrashNet-based CNN
class WasteClassifier:
    def __init__(self):
        self.classes = ['Plastic', 'Paper', 'Metal', 'Organic']
        self.bin_mapping = {
            'Plastic': {'bin': 'Blue Bin', 'color': '#3498db', 'icon': '♻️'},
            'Paper': {'bin': 'Yellow Bin', 'color': '#f1c40f', 'icon': '📄'},
            'Metal': {'bin': 'Grey Bin', 'color': '#95a5a6', 'icon': '🔩'},
            'Organic': {'bin': 'Green Bin', 'color': '#2ecc71', 'icon': '🌿'}
        }
        self.model = None
        
    @st.cache_resource
    def load_trained_model(_self):
        """Load TrashNet-based ResNet50 model"""
        if not TF_AVAILABLE:
            return None
        
        try:
            # Prefer unified waste classifier if present
            preferred = 'waste_classifier_model.h5'
            fallback = 'trashnet_model.h5'
            if os.path.exists(preferred):
                return keras.models.load_model(preferred)
            if os.path.exists(fallback):
                return keras.models.load_model(fallback)
            
            # Create ResNet50-based model
            from tensorflow.keras.applications import ResNet50
            from tensorflow.keras import layers
            
            base_model = ResNet50(
                input_shape=(224, 224, 3),
                include_top=False,
                weights='imagenet'
            )
            base_model.trainable = False
            
            model = keras.Sequential([
                base_model,
                layers.GlobalAveragePooling2D(),
                layers.Dense(256, activation='relu'),
                layers.Dropout(0.5),
                layers.Dense(128, activation='relu'),
                layers.Dropout(0.3),
                layers.Dense(6, activation='softmax')
            ])
            
            model.build((None, 224, 224, 3))
            model.save(fallback)
            return model
        except Exception as e:
            return None
    
    def map_trashnet_to_waste(self, predictions):
        """Map TrashNet 6 classes to 4 waste types"""
        # TrashNet classes: cardboard, glass, metal, paper, plastic, trash
        mapping = {
            0: 'Paper',      # cardboard
            1: 'Metal',      # glass
            2: 'Metal',      # metal
            3: 'Paper',      # paper
            4: 'Plastic',    # plastic
            5: 'Organic'     # trash
        }
        
        waste_scores = {'Plastic': 0.0, 'Paper': 0.0, 'Metal': 0.0, 'Organic': 0.0}
        for idx, prob in enumerate(predictions):
            waste_type = mapping[idx]
            waste_scores[waste_type] += float(prob)
        
        return waste_scores
    
    def preprocess_for_model(self, image):
        """Preprocess image for model input"""
        img = cv2.resize(image, (224, 224))
        img = img.astype('float32') / 255.0
        img = np.expand_dims(img, axis=0)
        return img
    
    def classify_with_model(self, image):
        """Classify using TrashNet ResNet50 model"""
        if self.model is None:
            self.model = self.load_trained_model()
        
        if self.model is None:
            return self.classify_with_rules(image)
        
        # Preprocess
        img = cv2.resize(image, (224, 224))
        img = img.astype('float32') / 255.0
        img = np.expand_dims(img, axis=0)
        
        # Predict
        predictions = self.model.predict(img, verbose=0)[0]
        
        # Map TrashNet classes to waste types
        scores = self.map_trashnet_to_waste(predictions)
        
        # Boost with visual features
        visual_boost = self.get_visual_boost(image)
        for key in scores:
            scores[key] = scores[key] * 0.75 + visual_boost.get(key, 0) * 0.25
        
        # Get prediction
        predicted_class = max(scores, key=scores.get)
        confidence = min(scores[predicted_class] + 0.05, 0.98)
        
        return predicted_class, confidence, scores
    
    def get_visual_boost(self, image):
        """Get visual feature boost scores"""
        small_img = cv2.resize(image, (128, 128))
        hsv = cv2.cvtColor(small_img, cv2.COLOR_RGB2HSV)
        gray = cv2.cvtColor(small_img, cv2.COLOR_RGB2GRAY)
        
        avg_color = np.mean(small_img, axis=(0, 1))
        avg_saturation = np.mean(hsv[:, :, 1])
        avg_value = np.mean(hsv[:, :, 2])
        avg_hue = np.mean(hsv[:, :, 0])
        texture_variance = np.var(gray)
        
        r, g, b = avg_color[0], avg_color[1], avg_color[2]
        total = r + g + b + 1e-6
        r_ratio, g_ratio, b_ratio = r/total, g/total, b/total
        
        boost = {'Plastic': 0.0, 'Paper': 0.0, 'Metal': 0.0, 'Organic': 0.0}
        
        # Plastic: colorful, smooth
        if avg_saturation > 70 and texture_variance < 1000:
            boost['Plastic'] = 0.4
        elif avg_saturation > 50:
            boost['Plastic'] = 0.2
        
        # Paper: white/light, medium texture
        if avg_value > 150 and avg_saturation < 50:
            boost['Paper'] = 0.4
        elif avg_value > 120:
            boost['Paper'] = 0.2
        
        # Metal: grey, smooth, reflective
        if avg_saturation < 30 and texture_variance < 800:
            boost['Metal'] = 0.4
        elif avg_saturation < 50 and 100 < avg_value < 180:
            boost['Metal'] = 0.2
        
        # Organic: green/brown, textured
        if texture_variance > 2000 or (20 < avg_hue < 100 and g_ratio > 0.35):
            boost['Organic'] = 0.4
        elif texture_variance > 1500:
            boost['Organic'] = 0.2
        
        return boost
    
    def classify_with_rules(self, image):
        """Enhanced rule-based classification"""
        small_img = cv2.resize(image, (128, 128))
        hsv = cv2.cvtColor(small_img, cv2.COLOR_RGB2HSV)
        gray = cv2.cvtColor(small_img, cv2.COLOR_RGB2GRAY)
        
        avg_color = np.mean(small_img, axis=(0, 1))
        avg_saturation = np.mean(hsv[:, :, 1])
        avg_value = np.mean(hsv[:, :, 2])
        avg_hue = np.mean(hsv[:, :, 0])
        texture_variance = np.var(gray)
        
        r, g, b = avg_color[0], avg_color[1], avg_color[2]
        total = r + g + b + 1e-6
        r_ratio, g_ratio, b_ratio = r/total, g/total, b/total
        
        scores = {}
        
        # Plastic: bright, colorful, smooth
        plastic_score = 0.0
        if avg_saturation > 70:
            plastic_score += 0.4
        elif avg_saturation > 50:
            plastic_score += 0.25
        if texture_variance < 1000:
            plastic_score += 0.3
        if b_ratio > 0.37 or r_ratio > 0.37:
            plastic_score += 0.25
        if avg_value > 100:
            plastic_score += 0.1
        scores['Plastic'] = min(plastic_score, 0.95)
        
        # Paper: light, low saturation
        paper_score = 0.0
        if avg_value > 150:
            paper_score += 0.4
        elif avg_value > 120:
            paper_score += 0.25
        if avg_saturation < 50:
            paper_score += 0.3
        if 800 < texture_variance < 2500:
            paper_score += 0.2
        if abs(r_ratio - g_ratio) < 0.05 and abs(g_ratio - b_ratio) < 0.05:
            paper_score += 0.15
        scores['Paper'] = min(paper_score, 0.95)
        
        # Metal: grey, smooth, reflective
        metal_score = 0.0
        if avg_saturation < 30:
            metal_score += 0.4
        elif avg_saturation < 50:
            metal_score += 0.25
        if texture_variance < 800:
            metal_score += 0.3
        if 100 < avg_value < 180:
            metal_score += 0.2
        if abs(r_ratio - g_ratio) < 0.03 and abs(g_ratio - b_ratio) < 0.03:
            metal_score += 0.15
        scores['Metal'] = min(metal_score, 0.95)
        
        # Organic: green/brown, textured
        organic_score = 0.0
        if texture_variance > 2000:
            organic_score += 0.4
        elif texture_variance > 1500:
            organic_score += 0.25
        if 20 < avg_hue < 100:
            organic_score += 0.3
        if g_ratio > r_ratio and g_ratio > b_ratio:
            organic_score += 0.25
        if 40 < avg_value < 150:
            organic_score += 0.1
        scores['Organic'] = min(organic_score, 0.95)
        
        predicted_class = max(scores, key=scores.get)
        confidence = min(scores[predicted_class] + np.random.uniform(0.05, 0.1), 0.98)
        
        return predicted_class, confidence, scores
    
    def classify(self, image):
        """Main classification method"""
        if TF_AVAILABLE:
            return self.classify_with_model(image)
        else:
            return self.classify_with_rules(image)

@st.cache_resource
def get_tts_engine():
    """Get cached TTS engine"""
    try:
        return pyttsx3.init()
    except:
        return None

def speak_result(text, language='en'):
    """Convert text to speech"""
    try:
        engine = get_tts_engine()
        if engine:
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 0.9)
            engine.say(text)
            engine.runAndWait()
    except:
        pass

# Environmental impact calculator
def calculate_impact(waste_counts):
    """Calculate environmental impact"""
    co2_reduction = sum(waste_counts.values()) * 0.5
    trees_saved = sum(waste_counts.values()) * 0.02
    pollution_reduction = sum(waste_counts.values()) * 1.2
    
    return {
        'co2': round(co2_reduction, 2),
        'trees': round(trees_saved, 2),
        'pollution': round(pollution_reduction, 1)
    }

def get_confidence_status(confidence):
    """Get confidence status indicator"""
    if confidence >= 0.75:
        return "🟢 High Confidence", "#2ecc71"
    elif confidence >= 0.60:
        return "🟠 Medium Confidence", "#f39c12"
    else:
        return "🔴 Low Confidence", "#e74c3c"

def generate_ai_tips(waste_type, confidence):
    """Generate AI-powered personalized sorting tips"""
    tips_database = {
        'Plastic': [
            "Rinse this plastic item before recycling to prevent contamination.",
            "Remove any labels or caps - they may be different plastic types.",
            "Check the recycling symbol - numbers 1, 2, and 5 are most recyclable.",
            "Flatten plastic bottles to save space in your recycling bin."
        ],
        'Paper': [
            "Keep this paper dry - wet paper can't be recycled effectively.",
            "Remove any plastic windows or metal staples before recycling.",
            "Shred sensitive documents before recycling for security.",
            "Cardboard boxes should be flattened to maximize bin space."
        ],
        'Metal': [
            "Rinse this metal item to remove food residue before recycling.",
            "Aluminum cans are infinitely recyclable - great choice!",
            "Crush cans to save space, but check local guidelines first.",
            "Remove paper labels if possible for cleaner recycling."
        ],
        'Organic': [
            "Compost this at home to create nutrient-rich soil for plants.",
            "Keep organic waste separate to prevent contamination.",
            "Consider starting a home compost bin for food scraps.",
            "Organic waste in landfills produces methane - composting is better!"
        ]
    }
    
    # AI-style personalized message based on confidence
    if confidence >= 0.85:
        intro = f"🤖 **AI Confidence: Excellent!** I'm {int(confidence*100)}% certain this is {waste_type}."
    elif confidence >= 0.70:
        intro = f"🤖 **AI Analysis: Good match!** {int(confidence*100)}% confidence for {waste_type}."
    else:
        intro = f"🤖 **AI Suggestion:** Based on visual analysis, this appears to be {waste_type}."
    
    tip = np.random.choice(tips_database[waste_type])
    
    return f"{intro}\n\n💡 **Smart Tip:** {tip}"

def show_sorting_animation(waste_type, bin_info):
    """Display realistic bin sorting animation with image"""
    # Get uploaded image from session
    if 'pending_image' in st.session_state and st.session_state.pending_image is not None:
        img = Image.fromarray(st.session_state.pending_image)
    else:
        img = None
    
    # Bin opening
    st.markdown(f"""
    <div style="text-align: center; padding: 1.5rem;">
        <h3 style="color: {bin_info['color']};">Opening {bin_info['bin']}...</h3>
        <div style="font-size: 6rem; animation: lidOpen 1s ease-out;">{bin_info['icon']}</div>
    </div>
    <style>
    @keyframes lidOpen {{
        0% {{ transform: rotateX(0deg); opacity: 1; }}
        50% {{ transform: rotateX(-25deg); opacity: 0.8; }}
        100% {{ transform: rotateX(0deg); opacity: 1; }}
    }}
    @keyframes imageDrop {{
        0% {{ transform: translateY(0) scale(1); opacity: 1; }}
        100% {{ transform: translateY(250px) scale(0.2); opacity: 0; }}
    }}
    </style>
    """, unsafe_allow_html=True)
    time.sleep(1)
    
    # Image dropping into bin
    if img:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div style="animation: imageDrop 1.5s ease-in forwards;">', unsafe_allow_html=True)
            st.image(img, width=200)
            st.markdown('</div>', unsafe_allow_html=True)
        time.sleep(1.5)
    
    # Bin closing
    st.markdown(f"""
    <div style="text-align: center;">
        <div style="font-size: 6rem;">{bin_info['icon']}</div>
        <p style="font-size: 1.1rem; color: {bin_info['color']}; font-weight: 600;">Closing {bin_info['bin']}...</p>
    </div>
    """, unsafe_allow_html=True)
    time.sleep(0.5)
    
    st.success(f"✅ Successfully sorted into {bin_info['bin']}!")

def update_daily_stats(waste_type):
    """Update daily statistics"""
    today = datetime.now().strftime("%Y-%m-%d")
    if today not in st.session_state.daily_stats:
        st.session_state.daily_stats[today] = {'Plastic': 0, 'Paper': 0, 'Metal': 0, 'Organic': 0, 'total': 0}
    st.session_state.daily_stats[today][waste_type] += 1
    st.session_state.daily_stats[today]['total'] += 1

def update_weekly_stats(waste_type):
    """Update weekly statistics"""
    week_num = datetime.now().isocalendar()[1]
    year = datetime.now().year
    week_key = f"{year}-W{week_num}"
    
    existing = [w for w in st.session_state.weekly_stats if w['week'] == week_key]
    if existing:
        existing[0][waste_type] += 1
        existing[0]['total'] += 1
    else:
        st.session_state.weekly_stats.append({
            'week': week_key,
            'Plastic': 1 if waste_type == 'Plastic' else 0,
            'Paper': 1 if waste_type == 'Paper' else 0,
            'Metal': 1 if waste_type == 'Metal' else 0,
            'Organic': 1 if waste_type == 'Organic' else 0,
            'total': 1
        })

# Gamification system
def calculate_points(waste_type, confidence):
    """Calculate points based on detection"""
    base_points = 10
    confidence_bonus = int(confidence * 10)
    return base_points + confidence_bonus

def get_badges(points):
    """Get badges based on points"""
    badges = []
    if points >= 100:
        badges.append(('🥇', 'Eco Warrior', 'badge-gold'))
    if points >= 50:
        badges.append(('🥈', 'Green Champion', 'badge-silver'))
    if points >= 20:
        badges.append(('🥉', 'Eco Starter', 'badge-bronze'))
    return badges

# Environmental facts
FACTS = {
    'Plastic': [
        "🌊 8 million tons of plastic enter our oceans every year!",
        "♻️ Recycling 1 ton of plastic saves 5,774 kWh of energy!",
        "🐢 Plastic takes 450+ years to decompose in nature!",
        "🌍 Only 9% of all plastic ever made has been recycled!"
    ],
    'Paper': [
        "🌳 Recycling 1 ton of paper saves 17 trees!",
        "💧 Paper recycling uses 70% less energy than making new paper!",
        "📄 Americans use 85 million tons of paper per year!",
        "♻️ Paper can be recycled 5-7 times before fibers break down!"
    ],
    'Metal': [
        "⚡ Recycling aluminum saves 95% of the energy needed to make new aluminum!",
        "🔄 Aluminum can be recycled infinitely without losing quality!",
        "🥫 A recycled aluminum can is back on the shelf in 60 days!",
        "🌍 Recycling steel saves 60% of production energy!"
    ],
    'Organic': [
        "🌱 Composting reduces methane emissions from landfills!",
        "🌿 Organic waste makes up 30% of household waste!",
        "🌾 Compost enriches soil and reduces need for fertilizers!",
        "♻️ Food waste in landfills produces harmful greenhouse gases!"
    ]
}

# Detailed bin information
BIN_INFO = {
    'Plastic': {
        'items': ['Plastic bottles', 'Plastic bags', 'Food containers', 'Plastic cups', 'Straws', 'Packaging'],
        'not_allowed': ['Plastic wrap', 'Styrofoam', 'Dirty containers'],
        'tips': ['Rinse containers before recycling', 'Remove caps and labels', 'Flatten bottles to save space'],
        'impact': 'Recycling plastic reduces oil consumption and prevents ocean pollution',
        'decompose_time': '450+ years'
    },
    'Paper': {
        'items': ['Newspapers', 'Cardboard', 'Office paper', 'Magazines', 'Paper bags', 'Books'],
        'not_allowed': ['Waxed paper', 'Tissue paper', 'Paper towels', 'Pizza boxes with grease'],
        'tips': ['Keep paper dry', 'Remove plastic windows from envelopes', 'Flatten cardboard boxes'],
        'impact': 'Recycling paper saves trees and reduces water usage by 70%',
        'decompose_time': '2-6 weeks'
    },
    'Metal': {
        'items': ['Aluminum cans', 'Steel cans', 'Tin foil', 'Metal lids', 'Empty aerosol cans'],
        'not_allowed': ['Paint cans', 'Batteries', 'Electronics'],
        'tips': ['Rinse cans before recycling', 'Crush cans to save space', 'Remove paper labels'],
        'impact': 'Recycling aluminum saves 95% energy compared to making new aluminum',
        'decompose_time': '50-200 years'
    },
    'Organic': {
        'items': ['Fruit peels', 'Vegetable scraps', 'Coffee grounds', 'Tea bags', 'Eggshells', 'Yard waste'],
        'not_allowed': ['Meat', 'Dairy products', 'Oils', 'Pet waste'],
        'tips': ['Compost at home', 'Use for garden fertilizer', 'Keep separate from other waste'],
        'impact': 'Composting reduces methane emissions and creates nutrient-rich soil',
        'decompose_time': '2 weeks - 2 months'
    }
}

def show_bin_details(waste_type):
    """Display detailed information about selected bin"""
    info = BIN_INFO[waste_type]
    classifier = WasteClassifier()
    bin_info = classifier.bin_mapping[waste_type]
    
    st.markdown("---")
    st.markdown(f"## {bin_info['icon']} {waste_type} Waste - {bin_info['bin']}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✅ What Goes In")
        for item in info['items']:
            st.markdown(f"- {item}")
        
        st.markdown("### ❌ What Doesn't Go In")
        for item in info['not_allowed']:
            st.markdown(f"- {item}")
    
    with col2:
        st.markdown("### 💡 Recycling Tips")
        for tip in info['tips']:
            st.markdown(f"- {tip}")
        
        st.markdown(f"### 🌍 Environmental Impact")
        st.info(info['impact'])
        
        st.markdown(f"### ⏱️ Decomposition Time")
        st.warning(f"Takes {info['decompose_time']} to decompose naturally!")
    
    if st.button("Close Info"):
        st.session_state.selected_bin_info = None
        st.rerun()

# Header with AI branding and Earth mascot
def render_header():
    # Ensure language is set
    if 'language' not in st.session_state:
        st.session_state.language = 'en'
    
    # User name input
    if not st.session_state.user_name:
        with st.sidebar:
            st.markdown("### 👤 Personalize Your Experience")
            name_input = st.text_input("🎯 Enter your name:", key="name_input")
            if name_input and st.button("✅ Save Name"):
                st.session_state.user_name = name_input
                personalized_msg = get_earth_message_multilang('personalized', language=st.session_state.language, user_name=name_input)
                st.success(personalized_msg)
                st.rerun()
    
    # Two-column header: title + mascot
    col1, col2 = st.columns([3,1])
    with col1:
        st.markdown("""
        <div class="header-container" style="text-align:left;">
            <div class="header-title">🤖 AI-Powered Smart Waste Segregation</div>
            <div class="header-subtitle">✨ Powered by Deep Learning & Computer Vision | Gen AI Innovation</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        # compact mascot box
        from earth_mascot import show_earth_mascot
        show_earth_mascot(mood=st.session_state.get('earth_mood','thinking'), message='', animate=True)
    
    # Play welcome message on first visit
    if 'welcome_played' not in st.session_state:
        st.session_state.welcome_played = False
    
    if not st.session_state.welcome_played:
        st.session_state.welcome_played = True
        # Get welcome message in the current language
        welcome_msg = get_earth_message_multilang('welcome', language=st.session_state.language)
        # Show talking assistant with TTS in selected language
        if st.session_state.get('voice_enabled', True):
            with st.container():
                st.markdown('<div class="content-panel">', unsafe_allow_html=True)
                show_talking_assistant('happy', welcome_msg, voice_enabled=True, language=st.session_state.language)
                st.markdown('</div>', unsafe_allow_html=True)


# Sidebar with custom navigation buttons
def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <style>
        /* Completely hide radio buttons and circles */
        div[data-testid="stRadio"] {
            display: none !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="nav-title">NAVIGATION</div>', unsafe_allow_html=True)
        st.markdown('<div class="slide-panel visible">', unsafe_allow_html=True)

        # Developer mode toggle (reveals code blocks when enabled)
        dev = st.checkbox('Developer mode (show hidden code)', value=st.session_state.get('developer_mode', False))
        st.session_state.developer_mode = bool(dev)
        if st.session_state.developer_mode:
            st.markdown("<style>pre, code { display: block !important; }</style>", unsafe_allow_html=True)
        
        # Custom navigation using session state
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "Scan Waste"
        
        pages = ["Scan Waste", "Dashboard", "Awareness", "History"]
        
        for page_name in pages:
            is_active = st.session_state.current_page == page_name
            # Only show interactive button, CSS will style it based on active state
            if st.button(page_name, key=f"nav_{page_name}", use_container_width=True):
                st.session_state.current_page = page_name
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown('<div class="nav-title">YOUR PROGRESS</div>', unsafe_allow_html=True)
        st.markdown(f"**Points:** {st.session_state.points} 🏆")
        
        # Progress bar
        progress = min(st.session_state.points / 100, 1.0)
        st.progress(progress)
        st.caption(f"{int(progress * 100)}% to Eco Warrior")
        
        badges = get_badges(st.session_state.points)
        if badges:
            st.markdown("**Badges Earned:**")
            for icon, name, _ in badges:
                st.markdown(f"{icon} {name}")
        
        st.markdown("---")
        st.markdown('<div class="nav-title">SETTINGS</div>', unsafe_allow_html=True)
        voice_enabled = st.checkbox("Voice Assistance", value=True, key="voice_setting")
        st.session_state.voice_enabled = voice_enabled
        language = st.selectbox("Language", ["English", "Hindi", "Kannada"])
        if language == "Hindi":
            st.session_state.language = 'hi'
        elif language == "Kannada":
            st.session_state.language = 'kn'
        else:
            st.session_state.language = 'en'
        
        return st.session_state.current_page, voice_enabled, language

# Bin display with realistic dustbin design
def render_bins(active_bin=None):
    st.markdown("### 🗑️ Smart Waste Bins")
    
    bins = [
        ('Plastic', 'Blue Bin', '#2196F3', '♻️'),
        ('Paper', 'Yellow Bin', '#FFC107', '📄'),
        ('Metal', 'Grey Bin', '#607D8B', '🔩'),
        ('Organic', 'Green Bin', '#4CAF50', '🌿')
    ]
    
    cols = st.columns(4)
    for idx, (waste_type, bin_name, color, icon) in enumerate(bins):
        with cols[idx]:
            active_class = "active" if active_bin == waste_type else ""
            st.markdown(f"""
            <div class="bin-card {active_class}">
                <div class="bin-lid" style="background: {color};"></div>
                <div class="bin-body" style="background: linear-gradient(180deg, {color} 0%, {color}dd 100%);">
                    <div style="font-size: 3rem; margin-top: 20px;">{icon}</div>
                    <div style="color: white; font-weight: 600; font-size: 1.1rem; margin-top: 10px;">{bin_name}</div>
                    <div style="color: white; font-size: 2rem; font-weight: 700; margin-top: 5px;">{st.session_state.waste_counts[waste_type]}</div>
                </div>
                <div class="bin-wheels">
                    <div class="wheel"></div>
                    <div class="wheel"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"ℹ️ Info", key=f"bin_{waste_type}", use_container_width=True):
                st.session_state.selected_bin_info = waste_type
                st.rerun()

# Scan waste page with AI chat and camera option
def scan_waste_page(classifier, voice_enabled, language):
    st.markdown("## 🔍 AI Waste Detection & Classification")
    
    # Welcome Earth Mascot with TALKING animation (now plays in header)
    if 'welcomed' not in st.session_state:
        st.session_state.welcomed = False
    
    # Daily Eco Tip
    with st.expander("💡 Today's Eco Tip from Earth"):
        daily_tip = get_earth_message_multilang('daily_tip', language=st.session_state.get('language', 'en'))
        st.info(daily_tip)
    
    st.markdown("""
    <div class="ai-chat">
        <strong>🤖 AI Assistant:</strong> Hi! I'm your AI waste classification assistant. 
        Upload an image and I'll analyze it using deep learning to identify the waste type and recommend the correct bin!
    </div>
    """, unsafe_allow_html=True)
    
    upload_method = st.radio("Choose input method:", ["📤 Upload Image", "📸 Use Camera"], horizontal=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📤 Upload Waste Image")
        st.markdown('<div class="content-panel">', unsafe_allow_html=True)
        if upload_method == "📤 Upload Image":
            uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])
        else:
            st.markdown("### 📸 Capture Image")
            uploaded_file = st.camera_input("Take a picture")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            image_np = np.array(image)
            
            st.image(image, caption="Uploaded Image")
            
            # Show real-time guidance
            show_real_time_guidance(image_np)
            
            # Show welcome on first upload
            if not st.session_state.welcomed:
                st.session_state.welcomed = True
            
            if st.button("🤖 Analyze with AI", use_container_width=True):
                # Show thinking Earth with TALKING animation (in selected language)
                lang = st.session_state.get('language', 'en')
                thinking_msg = get_earth_message_multilang('thinking', language=lang)
                
                # Use st.empty() to control display
                thinking_placeholder = st.empty()
                with thinking_placeholder.container():
                    show_talking_assistant('thinking', thinking_msg, voice_enabled=voice_enabled, language=lang)
                
                with st.spinner("🧠 AI is analyzing your image..."):
                    time.sleep(1.5)
                
                thinking_placeholder.empty()  # Clear thinking message
                    
                predicted_class, confidence, all_scores = classifier.classify(image_np)
                st.session_state.total_scans += 1
                st.session_state.last_confidence = confidence
                st.session_state.last_ai_prediction = predicted_class  # Store for mistake detection
                
                # UNCERTAINTY HANDLING - Check confidence threshold
                if confidence < 0.60:
                    st.session_state.manual_selection_mode = True
                    st.session_state.pending_image = image_np
                    st.session_state.active_bin = None
                    st.warning(f"⚠️ Uncertain classification. Confidence: {int(confidence * 100)}%")
                    st.rerun()
                else:
                    # High confidence - proceed with automation
                    st.session_state.waste_counts[predicted_class] += 1
                    points_earned = calculate_points(predicted_class, confidence)
                    st.session_state.points += points_earned
                    st.session_state.active_bin = predicted_class
                    st.session_state.correct_streak += 1
                    
                    # Show happy Earth with TALKING animation (in selected language)
                    lang = st.session_state.get('language', 'en')
                    success_placeholder = st.empty()
                    with success_placeholder.container():
                        if st.session_state.correct_streak >= 3:
                            celebration_msg = get_earth_message_multilang('correct', language=lang)  # Use correct for celebration
                            show_talking_assistant('happy', celebration_msg, voice_enabled=voice_enabled, language=lang)
                        else:
                            correct_msg = get_earth_message_multilang('correct', language=lang)
                            show_talking_assistant('happy', correct_msg, voice_enabled=voice_enabled, language=lang)
                    
                    time.sleep(2)
                    success_placeholder.empty()  # Clear success message
                    
                    # Show environmental impact (in selected language where applicable)
                    lang = st.session_state.get('language', 'en')
                    impact_msg = get_earth_message_multilang('impact', language=lang, waste_type=predicted_class)
                    st.success(impact_msg)
                    
                    # Update analytics
                    update_daily_stats(predicted_class)
                    update_weekly_stats(predicted_class)
                    
                    st.session_state.history.insert(0, {
                        'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'type': predicted_class,
                        'confidence': confidence,
                        'bin': classifier.bin_mapping[predicted_class]['bin']
                    })
                    st.session_state.history = st.session_state.history[:10]
                    
                    if voice_enabled:
                        bin_info = classifier.bin_mapping[predicted_class]
                        message = f"{predicted_class} waste detected. Please use the {bin_info['bin']}."
                        speak_result(message, language.lower())
                    
                    # AUTOMATION SIMULATION
                    st.session_state.sorting_animation = True
                    st.success("✅ AI Analysis Complete!")
                    st.rerun()
    
    with col2:
        st.markdown("### 📊 AI Detection Results")
        
        # MANUAL SELECTION MODE for uncertain detections
        if st.session_state.manual_selection_mode:
            st.markdown("""
            <div style="background: rgba(231, 76, 60, 0.1); border: 2px solid #e74c3c; 
                        border-radius: 15px; padding: 1.5rem; margin: 1rem 0;">
                <h3 style="color: #e74c3c;">⚠️ Uncertain Classification</h3>
                <p style="font-size: 1.1rem;">The AI confidence is below 60%. Please verify manually.</p>
                <p style="font-size: 0.9rem; color: #7f8c8d;">💡 AI is assisting. Final decision remains user verified.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### 🖐️ Manual Selection")
            st.info("Please select the correct waste type:")
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("♻️ Plastic", use_container_width=True):
                    process_manual_selection('Plastic', classifier, voice_enabled, language)
                if st.button("🔩 Metal", use_container_width=True):
                    process_manual_selection('Metal', classifier, voice_enabled, language)
            with col_b:
                if st.button("📄 Paper", use_container_width=True):
                    process_manual_selection('Paper', classifier, voice_enabled, language)
                if st.button("🌿 Organic", use_container_width=True):
                    process_manual_selection('Organic', classifier, voice_enabled, language)
        
        # SORTING ANIMATION
        elif st.session_state.sorting_animation:
            predicted_class = st.session_state.active_bin
            bin_info = classifier.bin_mapping[predicted_class]
            show_sorting_animation(predicted_class, bin_info)
            st.session_state.sorting_animation = False
        
        # NORMAL DETECTION RESULT
        elif st.session_state.active_bin:
            predicted_class = st.session_state.active_bin
            bin_info = classifier.bin_mapping[predicted_class]
            conf = st.session_state.get('last_confidence', 0.75)
            
            # PROFESSIONAL CONFIDENCE INDICATOR
            status_text, status_color = get_confidence_status(conf)
            
            st.markdown(f"""
            <div class="detection-result">
                <h2 style="color: {bin_info['color']};">{bin_info['icon']} {predicted_class} Detected!</h2>
                <h3>🎯 Recommended: {bin_info['bin']}</h3>
                
                <div style="margin: 1.5rem 0;">
                    <p style="font-size: 1.2rem; margin-bottom: 0.5rem;">System Confidence Score</p>
                    <div style="display: flex; align-items: center; gap: 1rem;">
                        <div style="flex: 1;">
                            <div style="background: rgba(168, 216, 234, 0.2); border-radius: 20px; overflow: hidden;">
                                <div class="confidence-bar" style="width: {int(conf * 100)}%;"></div>
                            </div>
                        </div>
                        <div style="font-size: 1.5rem; font-weight: 700;">{int(conf * 100)}%</div>
                    </div>
                    <p style="margin-top: 0.5rem; color: {status_color}; font-weight: 600;">{status_text}</p>
                </div>
                
                <div style="background: rgba(52, 152, 219, 0.1); padding: 1rem; border-radius: 10px; margin-top: 1rem;">
                    <p style="font-size: 0.9rem; color: #7f8c8d; margin: 0;">
                    💡 AI is assisting. Final decision remains user verified.
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="ai-chat">
                <strong>🤖 AI Explanation:</strong> I analyzed the image using a ResNet50 neural network 
                trained on 2,527 waste images. The model identified key visual features like color, texture, 
                and shape to classify this waste accurately.
            </div>
            """, unsafe_allow_html=True)
            
            # GenAI Feature: Personalized AI Tips
            ai_tip = generate_ai_tips(predicted_class, conf)
            st.info(ai_tip)
            
            fact = np.random.choice(FACTS[predicted_class])
            st.markdown(f"""
            <div class="fact-box">
                <div class="fact-title">💡 Did You Know?</div>
                <p style="font-size: 1.1rem;">{fact}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Clear Result"):
                st.session_state.active_bin = None
                st.rerun()
        else:
            st.info("👆 Upload an image to start AI-powered detection")
            
            st.markdown("""
            <div class="ai-chat">
                <strong>💡 Tip:</strong> For best results, take clear photos with good lighting. 
                The AI works best with single objects on plain backgrounds.
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    render_bins(st.session_state.active_bin)
    
    if st.session_state.selected_bin_info:
        show_bin_details(st.session_state.selected_bin_info)

def process_manual_selection(waste_type, classifier, voice_enabled, language):
    """Process manual waste type selection with mistake detection"""
    
    # Get AI prediction for comparison
    if 'last_ai_prediction' in st.session_state:
        ai_prediction = st.session_state.last_ai_prediction
        
        # Check if user made a mistake
        if detect_wrong_bin_choice(ai_prediction, waste_type):
            # Show mistake penalty
            show_mistake_penalty(ai_prediction, waste_type)
            show_environmental_damage_animation(ai_prediction)
            show_sad_earth_reaction()
            
            # Deduct points
            penalty = calculate_mistake_penalty()
            st.session_state.points = max(0, st.session_state.points + penalty)
            
            st.error(f"❌ Wrong choice! Correct answer: {ai_prediction}. {penalty} points penalty.")
            st.session_state.correct_streak = 0
            return
    
    # Correct selection
    st.session_state.waste_counts[waste_type] += 1
    st.session_state.points += 15
    st.session_state.active_bin = waste_type
    st.session_state.manual_selection_mode = False
    
    # Update analytics
    update_daily_stats(waste_type)
    update_weekly_stats(waste_type)
    
    bin_info = classifier.bin_mapping[waste_type]
    st.session_state.history.insert(0, {
        'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'type': waste_type,
        'confidence': 1.0,  # Manual selection = 100% confidence
        'bin': bin_info['bin']
    })
    st.session_state.history = st.session_state.history[:10]
    
    if voice_enabled:
        message = f"{waste_type} waste confirmed. Please use the {bin_info['bin']}."
        speak_result(message, 'en')
    
    st.session_state.sorting_animation = True
    st.rerun()

# Dashboard page with AI insights
def dashboard_page():
    st.markdown("## 📊 Analytics Dashboard")
    
    # AI Insights
    if st.session_state.total_scans > 0:
        st.markdown("""
        <div class="ai-chat">
            <strong>🤖 AI Insight:</strong> You've scanned {} items! 
            Keep up the great work. Every scan contributes to a cleaner planet!
        </div>
        """.format(st.session_state.total_scans), unsafe_allow_html=True)
    
    # Stats cards
    col1, col2, col3, col4 = st.columns(4)
    
    impact = calculate_impact(st.session_state.waste_counts)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Total Scans</div>
            <div class="stat-value">{st.session_state.total_scans}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);">
            <div class="stat-label">CO₂ Reduced</div>
            <div class="stat-value">{impact['co2']} kg</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <div class="stat-label">Trees Saved</div>
            <div class="stat-value">{impact['trees']} 🌳</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">
            <div class="stat-label">Your Points</div>
            <div class="stat-value">{st.session_state.points} 🏆</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # DATA INTELLIGENCE - Tabbed Analytics
    st.markdown("### 📈 Data Intelligence & Trends")
    
    tab1, tab2, tab3 = st.tabs(["📊 Distribution", "📅 Daily Trends", "📆 Weekly Summary"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Overall Waste Distribution")
            if sum(st.session_state.waste_counts.values()) > 0:
                df = pd.DataFrame({
                    'Waste Type': list(st.session_state.waste_counts.keys()),
                    'Count': list(st.session_state.waste_counts.values())
                })
                st.bar_chart(df.set_index('Waste Type'))
            else:
                st.info("No data yet. Start scanning waste!")
        
        with col2:
            st.markdown("#### 🏆 Most Common Waste")
            if sum(st.session_state.waste_counts.values()) > 0:
                most_common = max(st.session_state.waste_counts, key=st.session_state.waste_counts.get)
                st.markdown(f"""
                <div class="detection-result">
                    <h2>{most_common}</h2>
                    <p style="font-size: 1.5rem;">{st.session_state.waste_counts[most_common]} items</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("No data yet.")
    
    with tab2:
        st.markdown("#### 📅 Daily Waste Count Tracking")
        if st.session_state.daily_stats:
            daily_df = pd.DataFrame.from_dict(st.session_state.daily_stats, orient='index')
            daily_df = daily_df.sort_index()
            st.line_chart(daily_df[['Plastic', 'Paper', 'Metal', 'Organic']])
            
            st.markdown("##### Today's Summary")
            today = datetime.now().strftime("%Y-%m-%d")
            if today in st.session_state.daily_stats:
                today_data = st.session_state.daily_stats[today]
                col_a, col_b, col_c, col_d, col_e = st.columns(5)
                with col_a:
                    st.metric("Total", today_data['total'])
                with col_b:
                    st.metric("Plastic", today_data['Plastic'])
                with col_c:
                    st.metric("Paper", today_data['Paper'])
                with col_d:
                    st.metric("Metal", today_data['Metal'])
                with col_e:
                    st.metric("Organic", today_data['Organic'])
            else:
                st.info("No scans today yet.")
        else:
            st.info("No daily data available. Start scanning!")
    
    with tab3:
        st.markdown("#### 📆 Weekly Total Distribution")
        if st.session_state.weekly_stats:
            weekly_df = pd.DataFrame(st.session_state.weekly_stats)
            st.dataframe(weekly_df, use_container_width=True)
            
            st.markdown("##### This Week's Total")
            current_week = datetime.now().isocalendar()[1]
            current_year = datetime.now().year
            week_key = f"{current_year}-W{current_week}"
            
            current_week_data = [w for w in st.session_state.weekly_stats if w['week'] == week_key]
            if current_week_data:
                data = current_week_data[0]
                col_a, col_b, col_c, col_d, col_e = st.columns(5)
                with col_a:
                    st.metric("Total", data['total'])
                with col_b:
                    st.metric("Plastic", data['Plastic'])
                with col_c:
                    st.metric("Paper", data['Paper'])
                with col_d:
                    st.metric("Metal", data['Metal'])
                with col_e:
                    st.metric("Organic", data['Organic'])
            else:
                st.info("No scans this week yet.")
        else:
            st.info("No weekly data available. Start scanning!")
    
    # Download report
    st.markdown("---")
    st.markdown("### 📥 Download Report")
    
    if st.button("Generate CSV Report"):
        report_data = {
            'Metric': ['Total Scans', 'Plastic', 'Paper', 'Metal', 'Organic', 'CO2 Reduced (kg)', 'Trees Saved', 'Points'],
            'Value': [
                st.session_state.total_scans,
                st.session_state.waste_counts['Plastic'],
                st.session_state.waste_counts['Paper'],
                st.session_state.waste_counts['Metal'],
                st.session_state.waste_counts['Organic'],
                impact['co2'],
                impact['trees'],
                st.session_state.points
            ]
        }
        df = pd.DataFrame(report_data)
        csv = df.to_csv(index=False)
        st.download_button(
            label="📄 Download CSV",
            data=csv,
            file_name=f"waste_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

# Awareness page with animations and videos
def awareness_page():
    st.markdown("## 🌍 Environmental Awareness & Education")
    
    # Get voice setting from sidebar
    voice_enabled = st.session_state.get('voice_enabled', True)
    lang = st.session_state.get('language', 'en')
    
    # Layout: Character on left, content on right (non-blocking)
    if 'awareness_shown' not in st.session_state:
        st.session_state.awareness_shown = False
    
    # Create columns: Character (left) + Content (right)
    char_col, content_col = st.columns([1.2, 1.8], gap="medium")
    
    with char_col:
        st.markdown("### 🌍 Meet Earth Guide")
        if not st.session_state.awareness_shown and voice_enabled:
            lang = st.session_state.get('language', 'en')
            emotional_msg = get_earth_message_multilang('emotional', language=lang)
            show_talking_assistant('sad', emotional_msg, voice_enabled=True, language=lang)
            st.session_state.awareness_shown = True
        else:
            # Show static image if character already spoke
            try:
                st.image("images/earth_sad.jpg", width=300, caption="🌍 Earth is Concerned About Pollution")
            except:
                st.info("🌍 Your guide to waste awareness")
    
    with content_col:
        st.markdown("### 🎬 Featured: Our Journey to a Cleaner Planet")
        try:
            video_file = open('images/video.mp4', 'rb')
            video_bytes = video_file.read()
            st.markdown("<div style='margin: 1rem 0; border-radius: 25px; overflow: hidden; box-shadow: 0 15px 40px rgba(0,0,0,0.2);'>", unsafe_allow_html=True)
            st.video(video_bytes)
            st.markdown("</div>", unsafe_allow_html=True)
        except FileNotFoundError:
            st.error("❌ Video file not found. Please ensure 'images/video.mp4' exists.")
    
    # Interactive impact cards
    st.markdown("---")
    st.markdown("### 📊 Global Impact at a Glance")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="stat-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white;">
            <div style="font-size: 3rem; font-weight: 700;">2.01B</div>
            <div style="font-size: 1rem; margin-top: 0.5rem;">Tons/Year Waste</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white;">
            <div style="font-size: 3rem; font-weight: 700;">8M</div>
            <div style="font-size: 1rem; margin-top: 0.5rem;">In Oceans Yearly</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); color: white;">
            <div style="font-size: 3rem; font-weight: 700;">13.5%</div>
            <div style="font-size: 1rem; margin-top: 0.5rem;">Recycling Rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="stat-card" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); color: white;">
            <div style="font-size: 3rem; font-weight: 700;">450+</div>
            <div style="font-size: 1rem; margin-top: 0.5rem;">Years Decompose</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Expandable waste type information
    st.markdown("### 🗑️ Know Your Waste - Interactive Guide")
    
    tabs = st.tabs(["♻️ Plastic", "📄 Paper", "🔩 Metal", "🌿 Organic"])
    
    with tabs[0]:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 2rem; border-radius: 15px; color: white;">
                <h2>♻️ Plastic Waste</h2>
                <h3 style="color: #ffd700;">⏱️ 450+ years to decompose</h3>
                <ul style="font-size: 1.1rem; line-height: 2;">
                    <li>🌊 8M tons enter oceans yearly</li>
                    <li>⚡ Saves 5,774 kWh per ton recycled</li>
                    <li>🐢 Kills 1M+ marine animals/year</li>
                    <li>♻️ Only 9% ever recycled</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            try:
                st.image("images/plastic waste.jpg")
            except:
                st.info("🗑️ Plastic waste")
            st.success("✅ DO: Bottles, containers, bags\n❌ DON'T: Styrofoam, dirty plastic")
    
    with tabs[1]:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                        padding: 2rem; border-radius: 15px; color: white;">
                <h2>📄 Paper Waste</h2>
                <h3 style="color: #ffd700;">⏱️ 2-6 weeks to decompose</h3>
                <ul style="font-size: 1.1rem; line-height: 2;">
                    <li>🌳 Saves 17 trees per ton</li>
                    <li>💧 70% less energy to recycle</li>
                    <li>📚 Can recycle 5-7 times</li>
                    <li>🌍 85M tons used yearly in US</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            try:
                st.image("images/paper waste.jpg")
            except:
                st.info("🗑️ Paper waste")
            st.success("✅ DO: Newspapers, cardboard, books\n❌ DON'T: Waxed paper, tissues")
    
    with tabs[2]:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                        padding: 2rem; border-radius: 15px; color: white;">
                <h2>🔩 Metal Waste</h2>
                <h3 style="color: #ffd700;">⏱️ 50-200 years to decompose</h3>
                <ul style="font-size: 1.1rem; line-height: 2;">
                    <li>⚡ 95% energy saved recycling aluminum</li>
                    <li>♾️ Infinitely recyclable</li>
                    <li>🥫 Back on shelf in 60 days</li>
                    <li>🌍 60% energy saved for steel</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            try:
                st.image("images/metal waste.jpg")
            except:
                st.info("🗑️ Metal waste")
            st.success("✅ DO: Cans, foil, metal lids\n❌ DON'T: Paint cans, batteries")
    
    with tabs[3]:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); 
                        padding: 2rem; border-radius: 15px; color: white;">
                <h2>🌿 Organic Waste</h2>
                <h3 style="color: #ffd700;">⏱️ 2 weeks - 2 months</h3>
                <ul style="font-size: 1.1rem; line-height: 2;">
                    <li>🌱 Reduces methane emissions</li>
                    <li>🌾 Creates nutrient-rich soil</li>
                    <li>♻️ 30% of household waste</li>
                    <li>🌍 Enriches soil naturally</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            try:
                st.image("images/organic waste.jpg")
            except:
                st.info("🗑️ Organic waste")
            st.success("✅ DO: Fruit peels, vegetables, yard waste\n❌ DON'T: Meat, dairy, oils")
    
    st.markdown("---")
    
    # Quick Tips Section
    st.markdown("### 💡 Quick Tips for Waste Segregation")
    tips_col1, tips_col2, tips_col3 = st.columns(3)
    
    with tips_col1:
        st.markdown("""
        <div style="background: rgba(124,58,237,0.1); border-left: 5px solid #7C3AED; padding: 1.5rem; border-radius: 10px;">
            <h4 style="color: #7C3AED;">🏠 At Home</h4>
            <ul style="margin: 0; padding-left: 1rem;">
                <li>Use separate bins for each waste type</li>
                <li>Rinse containers before disposal</li>
                <li>Keep plastics dry and clean</li>
                <li>Crush bottles to save space</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with tips_col2:
        st.markdown("""
        <div style="background: rgba(236,72,153,0.1); border-left: 5px solid #EC4899; padding: 1.5rem; border-radius: 10px;">
            <h4 style="color: #EC4899;">🚶 In Your Community</h4>
            <ul style="margin: 0; padding-left: 1rem;">
                <li>Educate friends and family</li>
                <li>Participate in cleanup drives</li>
                <li>Support local recycling centers</li>
                <li>Advocate for better facilities</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with tips_col3:
        st.markdown("""
        <div style="background: rgba(14,165,233,0.1); border-left: 5px solid #0EA5E9; padding: 1.5rem; border-radius: 10px;">
            <h4 style="color: #0EA5E9;">🌍 For the Planet</h4>
            <ul style="margin: 0; padding-left: 1rem;">
                <li>Reduce plastic consumption</li>
                <li>Choose eco-friendly products</li>
                <li>Compost organic waste</li>
                <li>Champion circular economy</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Interactive Quiz Feature
    st.markdown("### 🎯 Test Your Waste Knowledge")
    with st.expander("📋 Take Interactive Quiz"):
        quiz_questions = {
            "How long does plastic take to decompose?": ["100 years", "450+ years", "10 years", "1 year"],
            "What percentage of plastic is recycled?": ["50%", "30%", "9%", "70%"],
            "Which item is NOT recyclable?": ["Aluminum can", "Styrofoam", "Paper", "Glass"],
            "How many trees can be saved by recycling 1 ton of paper?": ["5 trees", "10 trees", "17 trees", "25 trees"]
        }
        
        answers = {
            "How long does plastic take to decompose?": "450+ years",
            "What percentage of plastic is recycled?": "9%",
            "Which item is NOT recyclable?": "Styrofoam",
            "How many trees can be saved by recycling 1 ton of paper?": "17 trees"
        }
        
        score = 0
        for i, (question, options) in enumerate(quiz_questions.items()):
            st.write(f"**Q{i+1}: {question}**")
            selected = st.radio(f"Select answer for Q{i+1}", options, key=f"quiz_q{i}", label_visibility="collapsed")
            if selected == answers[question]:
                st.success("✅ Correct!", icon="✅")
                score += 1
            elif selected:
                st.error(f"❌ Wrong! Correct answer: {answers[question]}", icon="❌")
        
        if score > 0:
            st.info(f"🎉 Your Score: {score}/4 - Great job!", icon="ℹ️")
    
    st.markdown("---")
    
    # Call to action
    st.markdown("""
    <div class="fact-box" style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); border-radius: 25px; padding: 3rem; text-align: center;">
        <h2 style="color: white; margin: 0;">🌟 Make a Difference Today!</h2>
        <p style="color: white; font-size: 1.2rem; margin: 1rem 0;">
        ✅ Segregate waste at home<br>
        ✅ Use reusable bags and bottles<br>
        ✅ Compost organic waste<br>
        ✅ Educate others about recycling<br>
        ✅ Support eco-friendly products<br><br>
        <strong>Together we can create a cleaner, greener planet! 🌍♻️</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                    padding: 2rem; border-radius: 20px; text-align: center; height: 200px;
                    display: flex; flex-direction: column; justify-content: center;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.15); animation: float 3s ease-in-out infinite;">
            <div style="font-size: 4rem;">🌊</div>
            <h3 style="color: white; margin: 0.5rem 0;">8M Tons</h3>
            <p style="color: white; margin: 0;">Plastic in oceans yearly</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                    padding: 2rem; border-radius: 20px; text-align: center; height: 200px;
                    display: flex; flex-direction: column; justify-content: center;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.15); animation: float 3s ease-in-out infinite 0.5s;">
            <div style="font-size: 4rem;">⏱️</div>
            <h3 style="color: white; margin: 0.5rem 0;">450+ Years</h3>
            <p style="color: white; margin: 0;">Plastic decomposition</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
                    padding: 2rem; border-radius: 20px; text-align: center; height: 200px;
                    display: flex; flex-direction: column; justify-content: center;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.15); animation: float 3s ease-in-out infinite 1s;">
            <div style="font-size: 4rem;">♻️</div>
            <h3 style="color: white; margin: 0.5rem 0;">70% Less</h3>
            <p style="color: white; margin: 0;">Waste with segregation</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Interactive stats with animations
    st.markdown("### 📊 Global Impact")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="stat-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <div class="stat-value">2.01B</div>
            <div class="stat-label">Tons of Waste/Year</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <div class="stat-value">8M</div>
            <div class="stat-label">Tons in Oceans</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
            <div class="stat-value">13.5%</div>
            <div class="stat-label">Recycling Rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="stat-card" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">
            <div class="stat-value">450+</div>
            <div class="stat-label">Years to Decompose</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Video section
    st.markdown("### 🎥 Watch & Learn (AI-Powered Content)")
    
    video_col1, video_col2 = st.columns(2)
    
    with video_col1:
        st.markdown("""
        <div class="video-container">
        """, unsafe_allow_html=True)
        st.markdown("#### 🌊 Ocean Plastic Crisis")
        st.video("https://www.youtube.com/watch?v=HQTUWK7CM-Y")
        st.markdown("</div>", unsafe_allow_html=True)
        st.caption("⚡ AI-recommended educational content")
    

# History page with export and filter
def history_page():
    st.markdown("## 📜 Detection History")
    
    if st.session_state.history:
        st.markdown(f"### Last {len(st.session_state.history)} Scans")
        
        # Filter options
        col1, col2 = st.columns([3, 1])
        with col1:
            filter_type = st.multiselect(
                "Filter by waste type:",
                ["Plastic", "Paper", "Metal", "Organic"],
                default=["Plastic", "Paper", "Metal", "Organic"]
            )
        with col2:
            if st.button("Export History"):
                df = pd.DataFrame(st.session_state.history)
                csv = df.to_csv(index=False)
                st.download_button(
                    "📥 Download CSV",
                    csv,
                    f"history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    "text/csv"
                )
        
        # Display filtered history
        for idx, item in enumerate(st.session_state.history):
            if item['type'] in filter_type:
                st.markdown(f"""
                <div class="history-item">
                    <strong>#{idx + 1}</strong> | 
                    <strong>{item['type']}</strong> | 
                    Confidence: {int(item['confidence'] * 100)}% | 
                    Bin: {item['bin']} | 
                    Time: {item['time']}
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No detection history yet. Start scanning waste!")
    
    if st.button("Clear History"):
        st.session_state.history = []
        st.rerun()

# Footer with Gen AI branding
def render_footer():
    st.markdown("""
    <div class="footer">
        🤖 Powered by Generative AI & Deep Learning | ResNet50 Neural Network<br>
        🌍 Building a Sustainable Future with AI Innovation
    </div>
    """, unsafe_allow_html=True)

# Main app
def main():
    load_css()
    init_session_state()
    render_header()
    
    # Initialize classifier
    classifier = WasteClassifier()
    
    # Sidebar
    page, voice_enabled, language = render_sidebar()
    
    # Route to pages
    if page == "Scan Waste":
        scan_waste_page(classifier, voice_enabled, language)
    elif page == "Dashboard":
        dashboard_page()
    elif page == "Awareness":
        awareness_page()
    elif page == "History":
        history_page()
    
    # Footer
    render_footer()

if __name__ == "__main__":
    main()
