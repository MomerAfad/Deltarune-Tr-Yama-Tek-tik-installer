"""
Icon Creator for Deltarune Turkish Patch Installer

This script creates the blue pixel heart icon.
If you have the icon image already, save it as 'icon.png' in this folder first.

Usage:
1. If you have Pillow installed: python create_icon.py
2. If not: pip install pillow
   Then: python create_icon.py
"""

try:
    from PIL import Image
    import os
    
    # Check if user provided icon.png
    if os.path.exists('icon.png'):
        print("Found icon.png, converting to .ico format...")
        img = Image.open('icon.png')
        img.save('icon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
        print("✓ Icon converted successfully!")
        print("✓ icon.ico created!")
    else:
        print("Creating blue pixel heart icon...")
        # Create a blue pixel heart icon
        icon_size = 256
        img = Image.new('RGBA', (icon_size, icon_size), (0, 0, 0, 0))
        pixels = img.load()
        
        # Define the heart pattern (scaled up)
        pixel_scale = 16
        heart_pattern = [
            "  ##  ##  ",
            " #### ####",
            "##########",
            "##########",
            " ######## ",
            "  ######  ",
            "   ####   ",
            "    ##    "
        ]
        
        # Blue color
        blue = (45, 90, 255, 255)
        
        # Draw the heart
        for y, row in enumerate(heart_pattern):
            for x, char in enumerate(row):
                if char == '#':
                    for py in range(pixel_scale):
                        for px in range(pixel_scale):
                            actual_x = x * pixel_scale + px + 32
                            actual_y = y * pixel_scale + py + 64
                            if actual_x < icon_size and actual_y < icon_size:
                                pixels[actual_x, actual_y] = blue
        
        # Save as ICO with multiple sizes
        img.save('icon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
        img.save('icon.png', format='PNG')
        print("✓ Icon created successfully!")
        print("✓ icon.ico and icon.png saved!")

except ImportError:
    print("❌ PIL/Pillow not installed!")
    print("\nTo create the icon, you have two options:")
    print("\nOption 1 - Install Pillow:")
    print("  Run: pip install pillow")
    print("  Then run this script again: python create_icon.py")
    print("\nOption 2 - Manual conversion:")
    print("  1. Save your blue heart image as 'icon.png' in this folder")
    print("  2. Use online converter: https://convertio.co/png-ico/")
    print("  3. Download and save as 'icon.ico' in this folder")
    print("\nThe installer will automatically use icon.ico when available!")
except Exception as e:
    print(f"❌ Error: {e}")
