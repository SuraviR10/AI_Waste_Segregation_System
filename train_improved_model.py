"""
Improved waste classification model training with realistic data
Downloads real waste images from TrashNet dataset or creates enhanced synthetic data
Much better accuracy than simple color-based training
"""

import os
import sys
import numpy as np
import cv2
import shutil
from pathlib import Path
import urllib.request
import zipfile

try:
    import tensorflow as tf  # type: ignore
    from tensorflow import keras  # type: ignore
    from tensorflow.keras import layers  # type: ignore
    from tensorflow.keras.applications import EfficientNetB0  # type: ignore
    from tensorflow.keras.preprocessing.image import ImageDataGenerator  # type: ignore
    from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, EarlyStopping  # type: ignore
except ImportError as e:
    print(f"❌ TensorFlow not installed. Install with: pip install tensorflow")
    print(f"Error: {e}")
    sys.exit(1)

def download_trashnet_dataset():
    """
    Download TrashNet dataset - real-world waste images
    Source: https://github.com/garythung/trashnet
    """
    print("📥 Downloading TrashNet dataset (real waste images)...")
    
    dataset_dir = Path('dataset_real')
    if dataset_dir.exists():
        print(f"✅ Dataset already exists at {dataset_dir}")
        return dataset_dir
    
    try:
        # TrashNet dataset URL
        url = "https://github.com/garythung/trashnet/raw/master/data/dataset-resized.zip"
        zip_path = "trashnet_dataset.zip"
        
        print(f"⏳ Downloading from {url}...")
        urllib.request.urlretrieve(url, zip_path, reporthook=_download_progress)
        
        print(f"\n📦 Extracting dataset...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall()
        
        # Rename to standard location
        if Path('dataset-resized').exists():
            shutil.move('dataset-resized', str(dataset_dir))
        
        os.remove(zip_path)
        print(f"✅ TrashNet dataset ready at {dataset_dir}")
        return dataset_dir
        
    except Exception as e:
        print(f"⚠️  Could not download TrashNet dataset: {e}")
        print("📝 Fallback: Creating enhanced synthetic data instead...")
        return None

def _download_progress(block_num, block_size, total_size):
    """Show download progress"""
    downloaded = block_num * block_size
    percent = min(downloaded * 100 // total_size, 100)
    print(f"  [{percent}%] Downloaded {downloaded}/{total_size} bytes", end='\r')

def create_enhanced_synthetic_dataset():
    """
    Create REALISTIC synthetic waste images using computer vision techniques
    Much better than simple colored blocks
    """
    print("\n🎨 Creating enhanced synthetic waste dataset...")
    
    dataset_dir = Path('dataset/train')
    
    classes = {
        'Plastic': {
            'colors': [(100, 150, 255), (255, 100, 150), (150, 255, 100), (200, 100, 200)],
            'patterns': ['striped', 'dotted', 'shiny'],
            'shapes': ['bottle', 'bag', 'cup', 'container']
        },
        'Paper': {
            'colors': [(240, 240, 230), (250, 250, 240), (230, 230, 220), (200, 200, 190)],
            'patterns': ['wrinkled', 'textured', 'crumpled'],
            'shapes': ['sheet', 'box', 'roll', 'crumpled']
        },
        'Metal': {
            'colors': [(180, 180, 180), (160, 160, 160), (200, 200, 200), (220, 180, 140)],
            'patterns': ['shiny', 'dented', 'ridged'],
            'shapes': ['can', 'foil', 'bracket', 'cylinder']
        },
        'Organic': {
            'colors': [(80, 150, 60), (150, 100, 50), (100, 180, 70), (120, 60, 40)],
            'patterns': ['decomposed', 'wet', 'rough'],
            'shapes': ['leaf', 'fruit', 'waste', 'pile']
        }
    }
    
    images_per_class = 300  # Much more training data
    
    for class_name, props in classes.items():
        class_dir = dataset_dir / class_name
        class_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\n  Creating {class_name} class...")
        
        for i in range(images_per_class):
            # Random base color
            base_color = props['colors'][i % len(props['colors'])]
            
            # Create high-res image
            img = np.full((224, 224, 3), base_color, dtype=np.uint8)
            
            # Add complex texture based on material
            pattern = props['patterns'][i % len(props['patterns'])]
            
            if pattern == 'wrinkled':  # Paper
                # Create wrinkle lines
                for _ in range(8):
                    x1, y1 = np.random.randint(0, 224, 2)
                    x2, y2 = np.random.randint(0, 224, 2)
                    color = tuple(int(c * np.random.uniform(0.85, 1.15)) for c in base_color)
                    color = tuple(max(0, min(255, s)) for s in color)
                    cv2.line(img, (x1, y1), (x2, y2), color, np.random.randint(1, 3))
                
                # Random noise for paper texture
                noise = np.random.randint(-20, 20, (224, 224, 3), dtype=np.int16)
                img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
            
            elif pattern == 'shiny':  # Metal/Plastic
                # Create shine effects with bright spots
                for _ in range(3):
                    center = (np.random.randint(30, 194), np.random.randint(30, 194))
                    radius = np.random.randint(10, 30)
                    shine_color = tuple(min(255, int(c * 1.4)) for c in base_color)
                    cv2.circle(img, center, radius, shine_color, -1)
                
                # Add subtle reflection lines
                for _ in range(3):
                    x1, y1 = np.random.randint(0, 224), np.random.randint(0, 112)
                    x2, y2 = x1 + np.random.randint(-50, 50), y1 + np.random.randint(50, 150)
                    shine_color = tuple(min(255, int(c * 1.3)) for c in base_color)
                    cv2.line(img, (x1, y1), (x2, y2), shine_color, 1)
            
            elif pattern == 'dented':  # Metal
                # Create dent patterns
                for _ in range(5):
                    center = (np.random.randint(50, 174), np.random.randint(50, 174))
                    radius = np.random.randint(15, 40)
                    dark_color = tuple(int(c * 0.7) for c in base_color)
                    cv2.circle(img, center, radius, dark_color, np.random.randint(1, 3))
            
            elif pattern == 'dotted':  # Plastic
                # Create dot pattern
                for _ in range(20):
                    center = (np.random.randint(10, 214), np.random.randint(10, 214))
                    color = tuple(int(c * np.random.uniform(0.7, 1.3)) for c in base_color)
                    color = tuple(max(0, min(255, s)) for s in color)
                    cv2.circle(img, center, np.random.randint(2, 8), color, -1)
            
            elif pattern == 'decomposed':  # Organic
                # Create irregular shapes for decomposed matter
                for _ in range(10):
                    x1, y1 = np.random.randint(0, 224, 2)
                    x2, y2 = np.random.randint(0, 224, 2)
                    dark_color = tuple(int(c * np.random.uniform(0.5, 0.9)) for c in base_color)
                    cv2.line(img, (x1, y1), (x2, y2), dark_color, np.random.randint(1, 4))
                
                # Heavy noise for organic texture
                noise = np.random.randint(-40, 40, (224, 224, 3), dtype=np.int16)
                img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
            
            # Add main object shapes
            shape = props['shapes'][i % len(props['shapes'])]
            
            if shape == 'bottle':
                # Draw bottle-like shape  
                pts = np.array([[112, 30], [140, 80], [130, 150], [94, 150], [84, 80]], np.int32)
                cv2.polylines(img, [pts], True, (50, 50, 50), 2)
            
            elif shape == 'can':
                # Draw cylinder/can
                cv2.ellipse(img, (112, 60), (40, 15), 0, 0, 360, (50, 50, 50), 2)
                cv2.rectangle(img, (72, 60), (152, 150), (50, 50, 50), 2)
                cv2.ellipse(img, (112, 150), (40, 15), 0, 0, 360, (50, 50, 50), 2)
            
            elif shape == 'leaf':
                # Draw leaf-like shape for organic
                pts = np.array([[112, 30], [140, 80], [112, 160], [84, 80]], np.int32)
                cv2.polylines(img, [pts], True, (20, 20, 20), 2)
            
            # Add random color variations
            if i % 3 == 0:
                # Brightness variation
                hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV).astype(np.float32)
                hsv[:, :, 2] = hsv[:, :, 2] * np.random.uniform(0.8, 1.2)
                hsv[:, :, 2] = np.clip(hsv[:, :, 2], 0, 255)
                img = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)
            
            # Add Gaussian blur for realism
            if i % 2 == 0:
                img = cv2.GaussianBlur(img, (3, 3), 0)
            
            # Save image
            filepath = class_dir / f"img_{i:03d}.jpg"
            cv2.imwrite(str(filepath), cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
            
            if (i + 1) % 50 == 0:
                print(f"    Generated {i + 1}/{images_per_class} images")
    
    print("\n✅ Enhanced synthetic dataset created!")
    return dataset_dir

def create_efficient_model():
    """
    Create improved model using EfficientNetB0 (better accuracy than MobileNetV2)
    """
    print("\n🧠 Creating EfficientNetB0 model (better accuracy)...")
    
    base_model = EfficientNetB0(
        input_shape=(224, 224, 3),
        include_top=False,
        weights='imagenet',
        alpha=1.0
    )
    base_model.trainable = False  # Freeze initially
    
    model = keras.Sequential([
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.2),
        layers.RandomZoom(0.2),
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(256, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.4),
        layers.Dense(128, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.3),
        layers.Dense(4, activation='softmax')
    ])
    
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def train_model(dataset_dir, epochs=30):
    """Train with strong augmentation and callbacks"""
    print(f"\n📚 Training on dataset: {dataset_dir}")
    
    model = create_efficient_model()
    
    # Create data generators with strong augmentation
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=30,
        width_shift_range=0.3,
        height_shift_range=0.3,
        shear_range=0.2,
        zoom_range=0.3,
        brightness_range=[0.7, 1.3],
        horizontal_flip=True,
        vertical_flip=True,
        fill_mode='nearest'
    )
    
    val_datagen = ImageDataGenerator(rescale=1./255)
    
    # Load training data
    train_generator = train_datagen.flow_from_directory(
        dataset_dir,
        target_size=(224, 224),
        batch_size=32,
        class_mode='categorical',
        subset='training'
    )
    
    val_generator = val_datagen.flow_from_directory(
        dataset_dir,
        target_size=(224, 224),
        batch_size=32,
        class_mode='categorical'
    )
    
    # Callbacks
    callbacks = [
        ModelCheckpoint(
            'waste_classifier_model.h5',
            monitor='val_accuracy',
            save_best_only=True,
            verbose=1
        ),
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=3,
            verbose=1,
            min_lr=1e-7
        ),
        EarlyStopping(
            monitor='val_accuracy',
            patience=5,
            restore_best_weights=True,
            verbose=1
        )
    ]
    
    # Train
    history = model.fit(
        train_generator,
        validation_data=val_generator,
        epochs=epochs,
        callbacks=callbacks,
        verbose=1
    )
    
    # Save final model
    model.save('waste_classifier_model_final.h5')
    shutil.copy('waste_classifier_model.h5', 'trashnet_model.h5')  # Backup
    
    print("\n✅ Model training complete!")
    print(f"📊 Final validation accuracy: {history.history['val_accuracy'][-1]*100:.2f}%")
    
    return model

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--epochs', type=int, default=30, help='Number of training epochs')
    parser.add_argument('--synthetic-only', action='store_true', help='Use synthetic data only')
    args = parser.parse_args()
    
    print("\n" + "="*70)
    print("IMPROVED WASTE CLASSIFICATION MODEL TRAINING")
    print("="*70)
    
    # Try to download real dataset first
    dataset_dir = None
    if not args.synthetic_only:
        dataset_dir = download_trashnet_dataset()
    
    # Use synthetic data if real dataset not available
    if dataset_dir is None:
        dataset_dir = create_enhanced_synthetic_dataset()
    
    # Train model
    model = train_model(dataset_dir, epochs=args.epochs)
    
    print("\n" + "="*70)
    print("🎉 MODEL TRAINING COMPLETE!")
    print("="*70)
    print(f"Model saved as: waste_classifier_model.h5")
    print(f"Backup saved as: trashnet_model.h5")
    print("\nUsage:")
    print("  - For quick testing:  python train_improved_model.py --epochs 5")
    print("  - For best accuracy:  python train_improved_model.py --epochs 30")
    print("  - Synthetic only:     python train_improved_model.py --synthetic-only")
