
# Project Structure:
#
# people_code_generator/
# ├── main.py (entry point)
# ├── requirements.txt
# ├── config.py (configuration settings)
# ├── database/
# │   ├── __init__.py
# │   ├── db_handler.py (database connection and operations)
# │   └── models.py (data models)
# ├── code_generator/
# │   ├── __init__.py
# │   └── generator.py (code generation logic)
# ├── pdf_creator/
# │   ├── __init__.py
# │   └── pdf_maker.py (PDF generation)
# ├── utils/
# │   ├── __init__.py
# │   └── helpers.py (utility functions)
# └── output/ (generated PDFs will be stored here)



Python project that generates unique codes for people in a database and creates PDF files with their images and personal data.

Features:

A> Unique Code Generator: Creates codes based on personal information with optional checksums
B> QR Code Generation: Each code is embedded in a QR code for easy scanning
C> PDF Creation: Produces professional PDFs with personal information and photos
D> Database Storage: Securely stores all personal information
E> Image Processing: Automatically processes and resizes photos

The PDFs will be saved in the output directory and include the person's photo, details, unique code, and QR code for easy identification.

How to Use the Project

This project creates a Python application that generates unique identification codes for people in a database and produces PDFs with their information and photos. Here's how to use it:

Setup:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

Optionally create a .env file for configuration settings (following the variables in config.py)

Adding people to the database:

python main.py add "John" "Doe" "1990-01-15" -e "john@example.com" -p "555-123-4567" -a "123 Main St" -ph "path/to/photo.jpg"

Generating codes and PDFs:

For a specific person:

python main.py generate -p 1

For all people in the database:

python main.py generate
