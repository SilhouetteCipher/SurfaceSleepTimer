from PIL import Image, ImageDraw

def create_icon():
    # Create a new image with a blue background
    img = Image.new('RGB', (256, 256), color = (0, 150, 255))
    
    # Create a drawing object
    draw = ImageDraw.Draw(img)
    
    # Draw a white circle (clock face)
    draw.ellipse([10, 10, 246, 246], fill=(255, 255, 255))
    
    # Draw clock hands
    draw.line([128, 128, 128, 40], fill=(0, 0, 0), width=8)  # Hour hand
    draw.line([128, 128, 200, 128], fill=(0, 0, 0), width=6)  # Minute hand
    
    # Save as .ico
    img.save('lock_timer_icon.ico', format='ICO', sizes=[(256, 256)])

create_icon()