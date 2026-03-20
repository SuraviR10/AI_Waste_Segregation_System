# 🌍 AI-Based Smart Waste Segregation System

An intelligent waste classification system powered by Computer Vision and Deep Learning that detects and classifies waste into **Plastic, Paper, Metal, and Organic** categories, providing real-time bin recommendations with voice assistance.

---

## 🎯 Features

### 🔍 Core Functionality
- **AI-Powered Detection**: Classifies waste using color and texture analysis
- **Real-time Classification**: Instant waste type identification
- **Confidence Scoring**: Shows detection confidence with visual indicators
- **Smart Bin Mapping**: Automatic bin recommendation (Blue/Yellow/Grey/Green)

### 🎨 Modern UI/UX
- **Futuristic Dashboard**: Gradient-based eco-themed design
- **Animated Bins**: Glowing effect when waste is detected
- **Live Counters**: Real-time waste statistics
- **Responsive Layout**: Clean, professional, expo-ready interface

### 🌱 Environmental Impact
- **CO₂ Reduction Tracker**: Calculates environmental impact
- **Trees Saved Counter**: Shows positive contribution
- **Educational Facts**: Dynamic waste-specific information

### 🎮 Gamification
- **Points System**: Earn points for each scan
- **Achievement Badges**: Eco Starter, Green Champion, Eco Warrior
- **Progress Tracking**: Visual progress indicators

### 📊 Analytics Dashboard
- **Waste Distribution Charts**: Visual data representation
- **Most Common Waste**: Statistical insights
- **CSV Report Export**: Download detailed reports
- **Detection History**: Last 10 scans with timestamps

### 🔊 Voice Assistance
- **Text-to-Speech**: Audio feedback for detections
- **Multi-language Support**: English and Hindi options
- **Toggle Control**: Enable/disable voice output

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Webcam (optional, for live detection)

### Step 1: Clone or Download
```bash
cd c:\Users\MIT\Desktop\project
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
streamlit run app.py
```

The application will automatically open in your default browser at `http://localhost:8501`

---

## 📖 Usage Guide

### 1️⃣ Scan Waste
1. Navigate to **"🔍 Scan Waste"** from the sidebar
2. Click **"Browse files"** to upload a waste image
3. Click **"🔍 Analyze Waste"** button
4. View detection results with:
   - Waste type classification
   - Confidence score
   - Bin recommendation
   - Environmental fact

### 2️⃣ View Dashboard
1. Navigate to **"📊 Dashboard"**
2. View statistics:
   - Total scans performed
   - CO₂ reduction estimate
   - Trees saved counter
   - Your earned points
3. Check waste distribution chart
4. Download CSV report

### 3️⃣ Learn About Waste
1. Navigate to **"🌍 Awareness"**
2. Explore tabs for each waste type
3. Read environmental facts
4. Understand recycling importance

### 4️⃣ Check History
1. Navigate to **"📜 History"**
2. View last 10 detections
3. See timestamps and confidence scores
4. Clear history if needed

---

## 🎨 Waste Classification

| Waste Type | Bin Color | Icon | Characteristics |
|------------|-----------|------|-----------------|
| **Plastic** | Blue | ♻️ | High saturation, smooth texture |
| **Paper** | Yellow | 📄 | Low saturation, light colors |
| **Metal** | Grey | 🔩 | Reflective, low saturation |
| **Organic** | Green | 🌿 | Brown/green tones, high texture |

---

## 🛠️ Technical Architecture

### Classification Algorithm
- **Feature Extraction**: Color space analysis (RGB, HSV)
- **Texture Analysis**: Variance-based texture detection
- **Rule-Based Classification**: Multi-factor scoring system
- **Confidence Calculation**: Weighted feature scoring

### Technology Stack
- **Frontend**: Streamlit with custom CSS
- **Image Processing**: OpenCV
- **Data Analysis**: Pandas, NumPy
- **Voice Output**: pyttsx3 (Text-to-Speech)
- **Visualization**: Streamlit charts

---

## 🎯 Confidence Threshold

- **High Confidence** (≥ 60%): Waste classified and counted
- **Low Confidence** (< 60%): "Uncertain detection" message shown
- **Visual Indicator**: Progress bar shows confidence level

---

## 🏆 Gamification System

### Points Calculation
- Base Points: 10 per scan
- Confidence Bonus: Up to 10 additional points
- Total: 10-20 points per detection

### Badges
- 🥉 **Eco Starter**: 20+ points
- 🥈 **Green Champion**: 50+ points
- 🥇 **Eco Warrior**: 100+ points

---

## 📊 Environmental Impact Calculation

### Formulas
- **CO₂ Reduction**: Total items × 0.5 kg
- **Trees Saved**: Total items × 0.02
- **Pollution Reduction**: Total items × 1.2%

---

## 🎨 Color Palette

- **Primary Green**: #2ecc71
- **Primary Blue**: #3498db
- **Dark Green**: #27ae60
- **Yellow**: #f1c40f
- **Grey**: #95a5a6
- **Gradient Backgrounds**: Purple-blue, Green-teal

---

## 🔧 Customization

### Modify Classification Rules
Edit the `classify()` method in `WasteClassifier` class (lines 200-250 in app.py)

### Change Bin Colors
Update `bin_mapping` dictionary (lines 180-185 in app.py)

### Add New Facts
Extend the `FACTS` dictionary (lines 300-330 in app.py)

### Adjust Confidence Threshold
Modify the threshold check (line 650 in app.py):
```python
if confidence >= 0.6:  # Change 0.6 to your desired threshold
```

---

## 📁 Project Structure

```
project/
│
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── README.md             # Documentation
└── .streamlit/           # Streamlit config (auto-created)
```

---

## 🐛 Troubleshooting

### Issue: TTS not working
**Solution**: pyttsx3 may fail silently. Voice feature is optional and won't break the app.

### Issue: Image not loading
**Solution**: Ensure image format is JPG, JPEG, or PNG. Check file size < 200MB.

### Issue: Port already in use
**Solution**: Run with custom port:
```bash
streamlit run app.py --server.port 8502
```

### Issue: Module not found
**Solution**: Reinstall dependencies:
```bash
pip install -r requirements.txt --upgrade
```

---

## 🌟 Best Practices for Demo

1. **Use Clear Images**: Well-lit, focused waste images
2. **Test Different Types**: Show variety (plastic bottle, paper, can, food)
3. **Highlight Features**: Demonstrate voice, gamification, dashboard
4. **Show Impact**: Emphasize environmental statistics
5. **Explain AI**: Mention color/texture analysis approach

---

## 📈 Future Enhancements

- [ ] Live camera feed integration
- [ ] Deep learning model (YOLO/MobileNet)
- [ ] Multi-object detection
- [ ] Cloud database integration
- [ ] Mobile app version
- [ ] QR code bin tracking
- [ ] Community leaderboard

---

## 🤝 Contributing

This is an educational project. Feel free to:
- Add more waste categories
- Improve classification accuracy
- Enhance UI/UX design
- Add new features

---

## 📄 License

This project is created for educational purposes. Free to use and modify.

---

## 👨‍💻 Developer Notes

### Classification Logic
The system uses a simplified rule-based approach instead of deep learning for:
- **Faster inference**: No model loading time
- **Lightweight**: Runs on any machine
- **Interpretable**: Easy to understand and modify
- **Demo-ready**: Consistent results for presentations

For production use, consider training a CNN model with a labeled dataset.

---

## 🎓 Educational Value

This project demonstrates:
- Computer Vision fundamentals
- Image processing techniques
- Feature extraction methods
- UI/UX design principles
- Environmental awareness
- Gamification strategies

---

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code comments
3. Test with sample images
4. Verify all dependencies are installed

---

## 🌍 Impact Statement

**"Every piece of waste segregated correctly is a step towards a cleaner, greener planet. This AI system empowers individuals to make informed decisions and contribute to environmental sustainability."**

---

## 🎉 Acknowledgments

- Streamlit for the amazing framework
- OpenCV for image processing capabilities
- The open-source community

---

**Made with 💚 for a Sustainable Future**

---

## Quick Start Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py

# Access in browser
# http://localhost:8501
```

---

**Project Status**: ✅ Ready for Demo/Expo

**Last Updated**: 2024
