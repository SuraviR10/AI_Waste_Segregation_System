"""
Generate sample test images for waste classification
Run this to create test images if you don't have real waste photos
"""

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

def create_sample_images():
    """Create synthetic waste images for testing"""
    
    # Create samples directory
    os.makedirs('sample_images', exist_ok=True)
    
    samples = [
        {
            'name': 'plastic_bottle.jpg',
            'color': (100, 150, 255),  # Blue-ish
            'label': 'PLASTIC BOTTLE',
            'texture': 'smooth'
        },
        {
            'name': 'paper_sheet.jpg',
            'color': (240, 240, 230),  # White-ish
            'label': 'PAPER',
            'texture': 'rough'
        },
        {
            'name': 'metal_can.jpg',
            'color': (180, 180, 180),  # Grey
            'label': 'METAL CAN',
            'texture': 'smooth'
        },
        {
            'name': 'organic_waste.jpg',
            'color': (80, 150, 60),  # Green
            'label': 'ORGANIC WASTE',
            'texture': 'rough'
        }
    ]
    
    for sample in samples:
        # Create base image
        img = np.full((400, 400, 3), sample['color'], dtype=np.uint8)
        
        # Add texture
        if sample['texture'] == 'rough':
            noise = np.random.randint(-30, 30, (400, 400, 3), dtype=np.int16)
            img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        
        # Add some variation
        cv2.circle(img, (200, 200), 100, 
                   tuple(int(c * 0.8) for c in sample['color']), -1)
        
        # Convert to PIL for text
        pil_img = Image.fromarray(img)
        draw = ImageDraw.Draw(pil_img)
        
        # Add label
        try:
            font = ImageFont.truetype("arial.ttf", 30)
        except:
            font = ImageFont.load_default()
        
        # Get text size and position
        bbox = draw.textbbox((0, 0), sample['label'], font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        position = ((400 - text_width) // 2, 350)
        
        # Draw text with background
        draw.rectangle([position[0]-10, position[1]-5, 
                       position[0]+text_width+10, position[1]+text_height+5],
                      fill=(0, 0, 0, 128))
        draw.text(position, sample['label'], fill=(255, 255, 255), font=font)
        
        # Save
        filepath = os.path.join('sample_images', sample['name'])
        pil_img.save(filepath)
        print(f"✅ Created: {filepath}")
    
    print(f"\n🎉 Sample images created in 'sample_images' folder!")
    print("📸 Use these images to test the waste classification system")

if __name__ == "__main__":
    create_sample_images()
