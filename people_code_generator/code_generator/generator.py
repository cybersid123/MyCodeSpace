"""
import random
import string
import hashlib
import qrcode
from io import BytesIO
from ..config import CODE_PREFIX, CODE_LENGTH, INCLUDE_CHECKSUM

class CodeGenerator:
    def __init__(self, db_handler):
        self.db_handler = db_handler
        
    def generate_unique_code(self, person_id, first_name, last_name, dob):
        """
        Generate a unique code for a person based on their details
        
        Args:
            person_id: The database ID of the person
            first_name: Person's first name
            last_name: Person's last name
            dob: Person's date of birth (as string in format YYYY-MM-DD)
            
        Returns:
            A unique code string
        """
        # Base part of the code
        base = f"{CODE_PREFIX}{person_id:04d}"
        
        # Add a portion based on name and DOB
        name_hash = hashlib.md5(f"{first_name}{last_name}{dob}".encode()).hexdigest()
        name_part = name_hash[:CODE_LENGTH]
        
        # Combine parts
        code = f"{base}-{name_part}"
        
        # Add checksum if configured
        if INCLUDE_CHECKSUM:
            checksum = self._calculate_checksum(code)
            code = f"{code}-{checksum}"
        
        # Ensure the code is unique in the database
        while self.db_handler.get_person_by_code(code):
            # If code exists, add a random suffix
            random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            code = f"{base}-{name_part}-{random_suffix}"
            if INCLUDE_CHECKSUM:
                checksum = self._calculate_checksum(code)
                code = f"{code}-{checksum}"
        
        return code
    
    def _calculate_checksum(self, code):
        """Calculate a simple checksum for the code"""
        # Sum of ASCII values of characters, mod 97
        checksum = sum(ord(c) for c in code) % 97
        return f"{checksum:02d}"
    
    def generate_qr_code(self, code):
        """
        Generate a QR code image for a given code
        
        Args:
            code: The unique code to encode in the QR
            
        Returns:
            BytesIO object containing the QR code image
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(code)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save QR code to BytesIO object
        buffer = BytesIO()
        img.save(buffer)
        buffer.seek(0)
        
        return buffer
"""
