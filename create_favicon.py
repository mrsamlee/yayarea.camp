#!/usr/bin/env python3
"""
Simple script to create a favicon from an emoji
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_favicon():
    # Create a 32x32 image with a camping emoji
    size = 32
    img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Try to use a system font that supports emojis
    try:
        # Try different font paths for emoji support
        font_paths = [
            '/System/Library/Fonts/Apple Color Emoji.ttc',  # macOS
            '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf',  # Linux
            'C:/Windows/Fonts/seguiemj.ttf',  # Windows
        ]
        
        font = None
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    font = ImageFont.truetype(font_path, 24)
                    break
                except:
                    continue
        
        if font is None:
            # Fallback to default font
            font = ImageFont.load_default()
            
    except:
        font = ImageFont.load_default()
    
    # Draw the camping emoji
    emoji = "🏕️"
    bbox = draw.textbbox((0, 0), emoji, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    draw.text((x, y), emoji, font=font, fill=(0, 0, 0, 255))
    
    # Save as ICO file
    img.save('favicon.ico', format='ICO', sizes=[(16, 16), (32, 32)])
    
    # Save as PNG files
    img_16 = img.resize((16, 16), Image.Resampling.LANCZOS)
    img_32 = img.resize((32, 32), Image.Resampling.LANCZOS)
    img_180 = img.resize((180, 180), Image.Resampling.LANCZOS)
    
    img_16.save('favicon-16x16.png')
    img_32.save('favicon-32x32.png')
    img_180.save('apple-touch-icon.png')
    
    print("✅ Favicon files created successfully!")
    print("Created files:")
    print("- favicon.ico")
    print("- favicon-16x16.png")
    print("- favicon-32x32.png")
    print("- apple-touch-icon.png")

if __name__ == "__main__":
    try:
        create_favicon()
    except ImportError:
        print("❌ PIL (Pillow) not installed. Install with: pip install Pillow")
    except Exception as e:
        print(f"❌ Error creating favicon: {e}")
        print("You can manually create favicon files or use an online generator.")
