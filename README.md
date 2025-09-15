# LibraryManagementSystem

A simple web application to manage your books through a digital library!

# What’s its Purpose?

The main purpose of this project is to create a digital library application where students, within a school setting, can manage books they’ve borrowed and returned. This project aims to simplify the process of performing these actions (borrowing and returning) by having a user-friendly interface and displaying relevant information to end users. To give students an easier time and smoother user experience to manage their books, I will implement a history feature which tracks each instance they borrow and return items.

# Requirements

- Python
- Any browser (eg. Chrome, Firefox, Safari)

Python is required in order to run the Django framework, so the latest version of Python is heavily recommended for stability and performance.

Having the PIP package manager is also necessary to install all the dependencies of this application. However you might already have this when you first installed Python!

Don’t have Python? Install it here: https://www.python.org/downloads/



Any browser should be compatible with this web application. So use what you regularly use or prefer the most!

# How do I run the application?

1. Download the ZIP file containing all of the versions and extract it
2. Navigate and open the latest version of DigitalLibrary (Version 4) in an IDE such as VSCode
3. In your terminal, create a virtual environment:

```
python -m venv venv
```

4. Activate the virtual environment (Windows)

```
venv\Scripts\activate
```

In Mac or Linux, this command is used:

```
source venv/bin/activate
```

5. Install the dependencies

```
pip install -r requirements.txt
```

6. Run the server

```
python manage.py runserver
```

7. In your browser, go to localhost:

```
http://127.0.0.1:8000/
```

The web application should be running now!

If you encountered any errors when creating a virtual environment, this link may be useful: 
https://www.w3schools.com/python/python_virtualenv.asp

When the application has started running, register a student account.

Or, login as an admin.
Logging in as an admin gives features like an admin dashboard and the ability to add books.

Admin Login:

`Username: admin`

`Password: admin`

# More

Documentation: https://docs.google.com/document/d/1Gq4MuZ9Bw4ebcaoYClaqzUJHbIpzhLPF2FyD4YA1rQw/edit?usp=sharing
