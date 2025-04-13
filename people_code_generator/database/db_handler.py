# Load environment variables from .env file
load_dotenv()

# Database configuration
DB_TYPE = os.getenv("DB_TYPE", "sqlite")
DB_NAME = os.getenv("DB_NAME", "people.db")
DB_USER = os.getenv("DB_USER", "")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "")
DB_PORT = os.getenv("DB_PORT", "")

# PDF configuration
PDF_OUTPUT_DIR = os.getenv("PDF_OUTPUT_DIR", "output")
PDF_TEMPLATE = os.getenv("PDF_TEMPLATE", "default")
COMPANY_LOGO = os.getenv("COMPANY_LOGO", "")
COMPANY_NAME = os.getenv("COMPANY_NAME", "Your Company")

# Code generation settings
CODE_PREFIX = os.getenv("CODE_PREFIX", "PID")
CODE_LENGTH = int(os.getenv("CODE_LENGTH", "8"))
INCLUDE_CHECKSUM = os.getenv("INCLUDE_CHECKSUM", "True").lower() == "true"

# Create output directory if it doesn't exist
if not os.path.exists(PDF_OUTPUT_DIR):
    os.makedirs(PDF_OUTPUT_DIR)
"""
