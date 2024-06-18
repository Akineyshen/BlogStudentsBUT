# WWW.BLOGBUT.PL

<b>Description:</b> The project is a website developed using the Django web framework. It includes various features and functionalities typical of a modern web application. The development environment and deployment specifics are outlined below.

<h2>Development Environment:</h2>

<b>Framework:</b> Django

<b>IDE:</b> PyCharm

<b>Hosting:</b> PythonAnywhere

<b>Domain Provider:</b> Home.pl

<b>Domain:</b> blogbut.pl


<h2>Features:</h2>

User authentication and authorization

Article management - Create, update, delete articles - Commenting system

Tagging system for articles

User profile management

CAPTCHA for forms to enhance security

Static and media files handling

Sitemap generation for SEO

PDF generation for articles

<h2>Technical Details:</h2>

<h3>Django Packages:</h3>

django==5.0.4

django-ckeditor==6.7.1

django-js-asset==2.2.0

django-ranged-response==0.2.0

django-simple-captcha==0.6.0

sqlparse==0.5.0

sphinx==7.3.7 for documentation

see tab Requirements

<h3>Static and Media Files:</h3>

Static files are served from the /static/ directory.

Media files are stored in the /media/ directory with subdirectories for article images, site images, and profile images.

<h3>PDF Generation:</h3>

Uses reportlab for PDF generation.

<h3>Database</h3>

The database is implemented using SQLite3.

<h2>Hosting and Deployment:</h2>

The website is hosted on PythonAnywhere, a popular hosting service for Python applications.

Static and media files are configured to be served correctly on the hosting environment.

<h3>Domain:</h3>
The domain blogbut.pl was purchased from Home.pl and is registered for one year.

<h3>Documentation:</h3>

The project documentation is built using Sphinx and includes all necessary technical details for development and deployment.

To view the documentation, navigate to /docs/ on the website once it’s properly set up.
