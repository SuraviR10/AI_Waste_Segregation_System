"""
TrashNet-based waste classifier using ResNet architecture
Dataset: 6 classes (glass, paper, cardboard, plastic, metal, trash)
"""

import os
import numpy as np
import cv2

try:
    from tensorflow import keras
    from tensorflow.keras.applications import ResNet50
    from tensorflow.keras import layers
    TF_AVAILABLE = True
except:
    TF_AVAILABLE = False

def create_trashnet_model():
    """Create ResNet50-based model for TrashNet dataset"""
    if not TF_AVAILABLE:
        return None
    
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
        layers.Dense(6, activation='softmax')  # 6 TrashNet classes
    ])
    
    model.build((None, 224, 224, 3))
    return model

def map_trashnet_to_waste_types(predictions):
    """
    Map TrashNet 6 classes to our 4 waste types
    TrashNet: glass, paper, cardboard, plastic, metal, trash
    Our types: Plastic, Paper, Metal, Organic
    """
    # Class indices from TrashNet
    # 0: cardboard, 1: glass, 2: metal, 3: paper, 4: plastic, 5: trash
    
    mapping = {
        0: 'Paper',      # cardboard -> Paper
        1: 'Metal',      # glass -> Metal (recyclable)
        2: 'Metal',      # metal -> Metal
        3: 'Paper',      # paper -> Paper
        4: 'Plastic',    # plastic -> Plastic
        5: 'Organic'     # trash -> Organic
    }
    
    # Aggregate scores
    waste_scores = {'Plastic': 0.0, 'Paper': 0.0, 'Metal': 0.0, 'Organic': 0.0}
    
    for idx, prob in enumerate(predictions):
        waste_type = mapping[idx]
        waste_scores[waste_type] += float(prob)
    
    return waste_scores

def load_or_create_model():
    """Load existing model or create new one"""
    if not TF_AVAILABLE:
        return None
    
    model_path = 'trashnet_model.h5'
    
    if os.path.exists(model_path):
        try:
            model = keras.models.load_model(model_path)
            return model
        except:
            pass
    
    # Create new model
    model = create_trashnet_model()
    if model:
        model.save(model_path)
    
    return model

if __name__ == "__main__":
    model = load_or_create_model()
    if model:
        print("✅ TrashNet model created successfully!")
        print(f"Model architecture: ResNet50-based")
        print(f"Classes: 6 (cardboard, glass, metal, paper, plastic, trash)")
        print(f"Mapped to: 4 waste types (Plastic, Paper, Metal, Organic)")
    else:
        print("❌ TensorFlow not available")
