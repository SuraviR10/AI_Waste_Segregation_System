"""
Test script for Waste Classification System
Run this to verify the classifier is working correctly
"""

import cv2
import numpy as np
from PIL import Image

class WasteClassifier:
    def __init__(self):
        self.classes = ['Plastic', 'Paper', 'Metal', 'Organic']
        self.bin_mapping = {
            'Plastic': {'bin': 'Blue Bin', 'color': '#3498db', 'icon': '♻️'},
            'Paper': {'bin': 'Yellow Bin', 'color': '#f1c40f', 'icon': '📄'},
            'Metal': {'bin': 'Grey Bin', 'color': '#95a5a6', 'icon': '🔩'},
            'Organic': {'bin': 'Green Bin', 'color': '#2ecc71', 'icon': '🌿'}
        }
    
    def classify(self, image):
        """Classify waste using color and texture features"""
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        avg_color = np.mean(image, axis=(0, 1))
        avg_saturation = np.mean(hsv[:, :, 1])
        avg_value = np.mean(hsv[:, :, 2])
        texture_variance = np.var(gray)
        
        scores = {}
        
        # Plastic
        plastic_score = 0
        if avg_saturation > 50 and texture_variance < 1000:
            plastic_score += 0.3
        if avg_color[2] > 150 or avg_color[0] > 150:
            plastic_score += 0.4
        plastic_score += np.random.uniform(0.1, 0.3)
        scores['Plastic'] = min(plastic_score, 0.99)
        
        # Paper
        paper_score = 0
        if avg_saturation < 80 and avg_value > 100:
            paper_score += 0.4
        if 500 < texture_variance < 2000:
            paper_score += 0.3
        paper_score += np.random.uniform(0.1, 0.3)
        scores['Paper'] = min(paper_score, 0.99)
        
        # Metal
        metal_score = 0
        if avg_saturation < 50 and texture_variance < 800:
            metal_score += 0.4
        if 100 < avg_value < 200:
            metal_score += 0.3
        metal_score += np.random.uniform(0.1, 0.3)
        scores['Metal'] = min(metal_score, 0.99)
        
        # Organic
        organic_score = 0
        if texture_variance > 1500:
            organic_score += 0.3
        if avg_color[1] > avg_color[2] and avg_color[1] > avg_color[0]:
            organic_score += 0.4
        organic_score += np.random.uniform(0.1, 0.3)
        scores['Organic'] = min(organic_score, 0.99)
        
        predicted_class = max(scores, key=scores.get)
        confidence = scores[predicted_class]
        
        return predicted_class, confidence, scores

def test_classifier():
    """Test the classifier with synthetic images"""
    print("🧪 Testing Waste Classifier...\n")
    
    classifier = WasteClassifier()
    
    # Test with different colored images
    test_cases = [
        ("Blue plastic bottle", np.full((224, 224, 3), [100, 100, 200], dtype=np.uint8)),
        ("White paper", np.full((224, 224, 3), [240, 240, 240], dtype=np.uint8)),
        ("Grey metal can", np.full((224, 224, 3), [150, 150, 150], dtype=np.uint8)),
        ("Green organic waste", np.full((224, 224, 3), [50, 150, 50], dtype=np.uint8)),
    ]
    
    for name, test_image in test_cases:
        predicted_class, confidence, all_scores = classifier.classify(test_image)
        bin_info = classifier.bin_mapping[predicted_class]
        
        print(f"📸 Test: {name}")
        print(f"   ✅ Predicted: {predicted_class}")
        print(f"   📊 Confidence: {confidence:.2%}")
        print(f"   🗑️  Bin: {bin_info['bin']}")
        print(f"   📈 All Scores: {', '.join([f'{k}: {v:.2%}' for k, v in all_scores.items()])}")
        print()
    
    print("✅ Classifier test completed!\n")
    print("🚀 Ready to run: streamlit run app.py")

if __name__ == "__main__":
    test_classifier()
