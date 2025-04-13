
"""
import os
from io import BytesIO
from PIL import Image
from datetime import datetime

def load_image_file(file_path):
    """Load an image file and return its binary data"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Image file not found: {file_path}")
    
    try:
        with open(file_path, 'rb') as f:
            return f.read()
    except Exception as e:
        raise IOError(f"Error reading image file: {e}")

def resize_image(image_data, max_width=500, max_height=500, format='JPEG'):
    """
    Resize an image while maintaining aspect ratio
    
    Args:
        image_data: Binary image data
        max_width: Maximum width in pixels
        max_height: Maximum height in pixels
        format: Output format (JPEG, PNG, etc.)
        
    Returns:
        Binary data of the resized image
    """
    try:
        img = Image.open(BytesIO(image_data))
        img.thumbnail((max_width, max_height))
        
        output = BytesIO()
        img.save(output, format=format)
        output.seek(0)
        
        return output.getvalue()
    except Exception as e:
        print(f"Error resizing image: {e}")
        return image_data

def parse_date(date_string):
    """Parse a date string into a datetime.date object"""
    formats = [
        '%Y-%m-%d',
        '%d/%m/%Y',
        '%m/%d/%Y',
        '%d-%m-%Y',
        '%m-%d-%Y'
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_string, fmt).date()
        except ValueError:
            continue
    
    raise ValueError(f"Could not parse date string: {date_string}")
"""
