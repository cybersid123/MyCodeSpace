"""
import argparse
import os
import sys
from datetime import datetime
from database.db_handler import DatabaseHandler
from database.models import Person
from code_generator.generator import CodeGenerator
from pdf_creator.pdf_maker import PDFCreator
from utils.helpers import load_image_file, resize_image, parse_date

def generate_code_and_pdf(person_id=None):
    """Generate unique code and PDF for a person or all people"""
    db = DatabaseHandler()
    code_generator = CodeGenerator(db)
    pdf_creator = PDFCreator()
    
    if person_id:
        # Process a single person
        person = db.get_person_by_id(person_id)
        if not person:
            print(f"Error: Person with ID {person_id} not found")
            return
        
        people = [person]
    else:
        # Process all people
        people = db.get_all_people()
        if not people:
            print("No people found in the database")
            return
    
    for person in people:
        # Skip if the person already has a code
        if person.unique_code:
            print(f"Person {person.id} already has a code: {person.unique_code}")
            
            # Ask if we should regenerate
            if person_id:  # Only ask for confirmation in single-person mode
                choice = input("Regenerate code? (y/n): ")
                if choice.lower() != 'y':
                    continue
        
        # Generate unique code
        code = code_generator.generate_unique_code(
            person.id, 
            person.first_name, 
            person.last_name, 
            person.date_of_birth.strftime('%Y-%m-%d')
        )
        
        # Update person with new code
        db.update_person_code(person.id, code)
        person.unique_code = code
        
        # Generate QR code
        qr_code = code_generator.generate_qr_code(code)
        
        # Create PDF
        pdf_path = pdf_creator.create_person_pdf(person, qr_code)
        
        print(f"Generated code {code} and PDF for {person.first_name} {person.last_name}")
        print(f"PDF saved to: {pdf_path}")

def add_person(first_name, last_name, dob, email=None, phone=None, address=None, photo_path=None):
    """Add a new person to the database"""
    db = DatabaseHandler()
    
    # Parse date of birth
    try:
        date_of_birth = parse_date(dob)
    except ValueError as e:
        print(f"Error: {e}")
        return
    
    # Process photo if provided
    photo_data = None
    if photo_path:
        try:
            photo_data = load_image_file(photo_path)
            # Resize image to save space
            photo_data = resize_image(photo_data)
        except (FileNotFoundError, IOError) as e:
            print(f"Warning: {e}")
    
    # Create person data dictionary
    person_data = {
        'first_name': first_name,
        'last_name': last_name,
        'date_of_birth': date_of_birth,
        'email': email,
        'phone': phone,
        'address': address,
        'photo': photo_data,
        'unique_code': None,  # Will be generated later
        'is_active': True
    }
    
    # Add person to database
    new_person = db.add_person(person_data)
    
    if new_person:
        print(f"Added person: {new_person.first_name} {new_person.last_name} (ID: {new_person.id})")
        
        # Ask if we should generate code now
        choice = input("Generate unique code and PDF now? (y/n): ")
        if choice.lower() == 'y':
            generate_code_and_pdf(new_person.id)
    else:
        print("Error adding person to database")

def main():
    parser = argparse.ArgumentParser(description='People Code and PDF Generator')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Generate command
    generate_parser = subparsers.add_parser('generate', help='Generate unique codes and PDFs')
    generate_parser.add_argument('-p', '--person', type=int, help='ID of the person to generate code for (optional)')
    
    # Add person command
    add_parser = subparsers.add_parser('add', help='Add a new person')
    add_parser.add_argument('first_name', help='First name')
    add_parser.add_argument('last_name', help='Last name')
    add_parser.add_argument('dob', help='Date of birth (YYYY-MM-DD)')
    add_parser.add_argument('-e', '--email', help='Email address')
    add_parser.add_argument('-p', '--phone', help='Phone number')
    add_parser.add_argument('-a', '--address', help='Address')
    add_parser.add_argument('-ph', '--photo', help='Path to photo file')
    
    args = parser.parse_args()
    
    if args.command == 'generate':
        generate_code_and_pdf(args.person)
    elif args.command == 'add':
        add_person(
            args.first_name,
            args.last_name,
            args.dob,
            args.email,
            args.phone,
            args.address,
            args.photo
        )
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
"""
