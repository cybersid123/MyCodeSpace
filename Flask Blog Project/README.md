A simple yet functional blog with user authentication, posts, and comments.
Features

✅ User registration & login (with Flask-Login)
✅ Create, edit, and delete blog posts
✅ Add comments to posts
✅ Database storage (SQLite)
✅ Bootstrap-based frontend


Setup:
Prerequisites

    Python 3.7+

    Flask (pip install flask flask-sqlalchemy flask-login flask-wtf)

Project Structure

/blog/  
│── app.py                # Main Flask app  
│── /static/              # CSS/JS/Images  
│── /templates/           # HTML files  
│   ├── base.html         # Base template  
│   ├── home.html         # Homepage (lists posts)  
│   ├── post.html         # Single post view  
│   ├── login.html        # Login page  
│   ├── register.html     # Registration page  
│   └── create_post.html  # Post creation form  
│── models.py             # Database models  
│── forms.py              # WTForms for user input  


Run the Project

python app.py  # This will create blog.db

Visit http://127.0.0.1:5000 in your browser.
