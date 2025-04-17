# Blog Students BUT
![Language](https://img.shields.io/badge/Language-Python-brightgreen?style=for-the-badge&logo=Python&color=3776ab&labelColor=FCFCFC)
![Framework](https://img.shields.io/badge/Framework-Django-brightgreen?style=for-the-badge&logo=Django&logoColor=3776ab&color=3776ab&labelColor=FCFCFC)
![Size](https://img.shields.io/github/repo-size/Akineyshen/BlogStudentsBUT?label=Size&style=for-the-badge&color=3776ab&labelColor=FCFCFC)
![Last Commit](https://img.shields.io/github/last-commit/Akineyshen/BlogStudentsBUT?label=Last%20Commit&style=for-the-badge&color=3776ab&labelColor=FCFCFC)

## Features
### Core Functionality
- **User Authentication**: Register, login, and manage user profiles  
- **Blog Posts**: Create, edit, view and delete blog posts  
- **Categories**: Organize posts by categories  
- **Comments**: Interactive commenting system on blog posts
- **Messaging System**: Private messaging between users with reply functionality
- **Responsive Design**: Mobile-friendly interface  
- **Search**: Advanced search through blog posts and users

### Advanced Features
- **PDF Generation**: Generate PDF versions of blog posts
- **Automated Documentation**: Sphinx integration for code documentation
- **Admin Features**: Comprehensive Django admin interface
- **Google Maps Integration**: Interactive maps
- **Post Privacy**: Option to make posts private or password-protected

## Requirements
- Python 3.8+
- Django 4.0+
- Additional packages in `requirements.txt`

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Akineyshen/BlogStudentsBUT.git
   ```
2. Navigate to the project directory:
   ```bash
    cd BlogStudentsBUT
    ```
3. Create virtual environment:
    ```bash
    python -m venv .venv
    ```
4. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5. Apply migrations:
    ```bash
    python manage.py migrate
    ```
6. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```
7. Run development server:
   ```bash
   python manage.py runserver
   ```

## Project Structure
```bash
   BlogStudentsBUT/
   ├── BlogStudentsBUT           # Main blog application
   ├── articles/                 # Blog articles
   ├── docs/                     # Documentation sources
   ├── media/                    # Media Files
   ├── source/                   # Source files
   ├── static/                   # Static files
   ├── templates/                # HTML templates
   ├── users/                    # User application
   ├── .gitignore                # Ignored files
   ├── db.sqlite3                # SQLite database
   ├── manage.py                 # Django management
   ├── README.md                 # Project description
   └── requirements.txt          # Python Dependencies
```

## Building Documentation
1. Install Sphinx:
   ```bash
   pip install sphinx sphinx_book_theme
   ```
2. Generate documentation:
   ```bash
   sphinx-build -b html source build/html
   ```
3. Open the generated documentation in a web browser:
   ```bash
    open build/html/index.html
    ```
   
## Screenshots
<img src="https://i.imgur.com/xRK7392.png" alt="Main Page">

<img src="https://i.imgur.com/OpiHtar.png" alt="Comment Page">

<img src="https://i.imgur.com/mFaqv6v.png" alt="Search Page">

<img src="https://i.imgur.com/AW1eljd.png" alt="Profile Page">

<img src="https://i.imgur.com/H8YGRtp.png" alt="Message Page">

