# AI-powered unique features for waste segregation

def generate_ai_suggestions(waste_counts):
    """Generate personalized AI suggestions"""
    suggestions = []
    total = sum(waste_counts.values())
    
    if total == 0:
        return ["🤖 Start scanning to get AI insights!"]
    
    most_common = max(waste_counts, key=waste_counts.get)
    
    if waste_counts['Plastic'] > total * 0.4:
        suggestions.append("🤖 AI Alert: High plastic usage detected. Switch to reusables!")
    
    if waste_counts['Organic'] < total * 0.1:
        suggestions.append("🤖 AI Tip: Start composting to reduce landfill by 30%!")
    
    if total > 10:
        suggestions.append(f"🤖 Achievement: {total} items scanned! Great impact!")
    
    return suggestions if suggestions else ["🤖 Keep up the great work!"]

def show_comparison_chart(waste_counts):
    """Show user vs global comparison"""
    import pandas as pd
    import streamlit as st
    
    user_total = sum(waste_counts.values())
    if user_total == 0:
        return
    
    user_pct = {k: (v/user_total)*100 for k, v in waste_counts.items()}
    global_avg = {'Plastic': 35, 'Paper': 25, 'Metal': 15, 'Organic': 25}
    
    df = pd.DataFrame({
        'Waste Type': list(user_pct.keys()),
        'Your %': list(user_pct.values()),
        'Global %': [global_avg[k] for k in user_pct.keys()]
    })
    
    st.bar_chart(df.set_index('Waste Type'))
    
    if user_pct['Plastic'] < global_avg['Plastic']:
        st.success("🤖 You're using less plastic than average!")
