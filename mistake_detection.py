"""
Mistake Detection & Real-Time Guidance Features
"""

import streamlit as st

def detect_wrong_bin_choice(predicted_type, user_selected_type):
    """Detect if user selected wrong bin"""
    return predicted_type != user_selected_type

def show_mistake_penalty(correct_type, wrong_type):
    """Show mistake detection with penalty"""
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
                padding: 2rem; border-radius: 20px; color: white; text-align: center;
                box-shadow: 0 15px 40px rgba(231,76,60,0.4); animation: shake 0.5s;">
        <div style="font-size: 5rem; animation: pulse 1s infinite;">❌</div>
        <h2 style="margin: 1rem 0;">Wrong Bin Choice!</h2>
        <p style="font-size: 1.3rem; margin: 1rem 0;">
            This is <strong>{wrong_type}</strong> waste, not {correct_type}!
        </p>
        <div style="background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 10px; margin: 1rem 0;">
            <p style="font-size: 1.1rem; margin: 0;">
                🚨 This causes recycling contamination!<br>
                💔 Damages the environment
            </p>
        </div>
        <p style="font-size: 1rem; color: #ffeb3b;">
            -10 Points Penalty
        </p>
    </div>
    
    <style>
    @keyframes shake {{
        0%, 100% {{ transform: translateX(0); }}
        25% {{ transform: translateX(-10px); }}
        75% {{ transform: translateX(10px); }}
    }}
    @keyframes pulse {{
        0%, 100% {{ transform: scale(1); }}
        50% {{ transform: scale(1.1); }}
    }}
    </style>
    """, unsafe_allow_html=True)

def show_environmental_damage_animation(waste_type):
    """Show environmental damage if 100 people made same mistake"""
    impacts = {
        'Plastic': {
            'contamination': '500 kg of recyclables contaminated',
            'ocean': '50 kg plastic enters ocean',
            'animals': '10 marine animals harmed',
            'energy': '2,887 kWh energy wasted'
        },
        'Paper': {
            'contamination': '850 kg of paper wasted',
            'trees': '8.5 trees cut unnecessarily',
            'water': '35,000 liters water wasted',
            'energy': '1,700 kWh energy wasted'
        },
        'Metal': {
            'contamination': '300 kg of metal wasted',
            'energy': '28,500 kWh energy wasted',
            'mining': 'Unnecessary mining required',
            'emissions': '150 kg CO₂ emissions'
        },
        'Organic': {
            'contamination': '1,000 kg organic waste to landfill',
            'methane': '50 kg methane gas produced',
            'soil': 'Lost opportunity for 500 kg compost',
            'emissions': '100 kg CO₂ equivalent'
        }
    }
    
    impact = impacts.get(waste_type, {})
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #34495e 0%, #2c3e50 100%);
                padding: 2rem; border-radius: 20px; color: white; margin: 1rem 0;">
        <h3 style="color: #e74c3c; margin-bottom: 1rem;">
            ⚠️ If 100 People Made This Mistake...
        </h3>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
            <div style="background: rgba(231,76,60,0.2); padding: 1rem; border-radius: 10px;">
                <p style="font-size: 0.9rem; margin: 0;">🗑️ {impact.get('contamination', 'N/A')}</p>
            </div>
            <div style="background: rgba(231,76,60,0.2); padding: 1rem; border-radius: 10px;">
                <p style="font-size: 0.9rem; margin: 0;">⚡ {impact.get('energy', 'N/A')}</p>
            </div>
            <div style="background: rgba(231,76,60,0.2); padding: 1rem; border-radius: 10px;">
                <p style="font-size: 0.9rem; margin: 0;">🌊 {impact.get('ocean', impact.get('water', 'N/A'))}</p>
            </div>
            <div style="background: rgba(231,76,60,0.2); padding: 1rem; border-radius: 10px;">
                <p style="font-size: 0.9rem; margin: 0;">💨 {impact.get('emissions', impact.get('methane', 'N/A'))}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_real_time_guidance(image):
    """Show real-time camera guidance before throwing"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
                padding: 2rem; border-radius: 20px; color: white; margin: 1rem 0;">
        <h3 style="margin-bottom: 1rem;">📷 Before You Throw - Quick Checks</h3>
        <div style="background: rgba(255,255,255,0.1); padding: 1.5rem; border-radius: 15px;">
            <div style="margin: 1rem 0;">
                <p style="font-size: 1.1rem; margin: 0.5rem 0;">
                    ✓ <strong>Rotate the object</strong> - Check all sides
                </p>
            </div>
            <div style="margin: 1rem 0;">
                <p style="font-size: 1.1rem; margin: 0.5rem 0;">
                    ✓ <strong>Remove food residue</strong> - Rinse if needed
                </p>
            </div>
            <div style="margin: 1rem 0;">
                <p style="font-size: 1.1rem; margin: 0.5rem 0;">
                    ✓ <strong>Separate components</strong> - Lid from bottle
                </p>
            </div>
            <div style="margin: 1rem 0;">
                <p style="font-size: 1.1rem; margin: 0.5rem 0;">
                    ✓ <strong>Check for labels</strong> - Remove if possible
                </p>
            </div>
        </div>
        <p style="text-align: center; margin-top: 1rem; font-size: 0.9rem; opacity: 0.8;">
            💡 AI Assistant: These steps prevent contamination
        </p>
    </div>
    """, unsafe_allow_html=True)

def calculate_mistake_penalty():
    """Calculate penalty for wrong bin choice"""
    return -10  # Deduct 10 points

def show_sad_earth_reaction():
    """Show Earth mascot sad reaction for mistake"""
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: rgba(231,76,60,0.1);
                border-radius: 20px; margin: 1rem 0;">
        <div style="font-size: 8rem; animation: cry 2s infinite;">😢🌍</div>
        <p style="font-size: 1.3rem; color: #e74c3c; font-weight: 600;">
            Earth is sad... Please learn from this mistake!
        </p>
    </div>
    
    <style>
    @keyframes cry {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(10px); }}
    }}
    </style>
    """, unsafe_allow_html=True)
