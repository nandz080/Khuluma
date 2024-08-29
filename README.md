Khuluma
Khuluma is a real-time messaging application built with Python, Django, JavaScript, Bootstrap, HTML, and CSS. The application enables users to create profiles, manage friendships, and engage in instant messaging. Khuluma is designed with a focus on simplicity, security, and user-friendliness. It is intended to be deployed on Heroku.

Table of Contents
Features
Technologies Used
Installation
Setup
Usage
Deployment
File Structure
License
Features

FEATURES
User authentication (sign up, login, logout)
Real-time messaging
User profile management
Friendship management adding and removing friends
Responsive design using Bootstrap
Secure password storage

User Management
User Signup/Login: Users can register and log in to the application.
Profile Management: Users can update their profiles, including changing profile pictures and other personal details.
Password Reset: Allows users to reset their password via email.
Social Authentication: Integration with Google and Facebook for easy sign-up and login.


Messaging
Instant Messaging: Real-time 1:1 messaging between users using WebSockets.
Friendship Management: Users can connect with others by adding them as friends.
Chat Interface: A clean and intuitive chat interface where users can view their message history and send/receive messages instantly.
Group Chat (Future Enhancement): Planned feature for allowing group messaging.
Other Features
Responsive Design: The app is built using Bootstrap, ensuring it works well on both desktop and mobile devices.
CSRF Protection: Secure handling of forms and user input with Django's CSRF protection.


Technologies Used
Backend: Python, Django
Frontend: JavaScript, HTML, CSS, Bootstrap
Database: SQLite (default for development, can be swapped for PostgreSQL in production)
WebSockets: Django Channels for real-time messaging
Deployment: Heroku
Installation
Prerequisites
Python 3.8 or higher
Django 4.0 or higher
Node.js (for managing JavaScript dependencies)
Git (for version control)


Clone the Repository
    git clone https://github.com/yourusername/khuluma.git
    cd khuluma
    Install Python Dependencies

NB! It's recommended to use a virtual environment:
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt

Install JavaScript Dependencies
    npm install

Setup
    Database Migrations
Apply the migrations to set up your database:
    python manage.py migrate
    Static Files
Collect static files:
    python manage.py collectstatic
    Create a Superuser
Create an admin user to manage the application:
    python manage.py createsuperuser
Running the Development Server
You can start the development server with:
    python manage.py runserver
    Access the application at http://127.0.0.1:8000/.

Usage
    User Registration and Login
    Users can register a new account or log in with an existing account. Upon registration, users can fill out their profile information and start connecting with other users.

Adding Friends
    Users can search for other users and send friend requests. Once a friend request is accepted, they can start messaging each other.

Instant Messaging
    Users can access the messaging interface via the "Messages" section, where they can view their chat history, send messages, and receive messages in real-time.

Deployment
    Heroku Deployment
    Ensure you have the Heroku CLI installed. To deploy the application to Heroku, follow these steps:

Log in to Heroku

File Structure
    The project directory structure is as follows:

Khuluma/
├── Khuluma/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── my_messages/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── templates/
│   │   └── chat/
│   │       ├── chat.html
│   │       └── chat_home.html
│   └── static/
│       └── css/
│           └── style.css
├── user/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── templates/
│   │   ├── registration/
│   │   │   ├── signup.html
│   │   │   └── login.html
│   │   └── profile/
│   │       └── profile_details.html
│   └── static/
│       └── img/
│           └── profile_pics/
└── manage.py

License
This project is licensed under the MIT License. See the LICENSE file for details.