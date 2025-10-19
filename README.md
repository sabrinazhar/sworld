# 🌐 Sworld

A Flask-based **social networking web application** that allows users to sign up, log in, create posts, follow other users, and explore shared content in a community-driven environment.  

The system implements a fully functional backend with authentication, database integration, and responsive user interfaces using Flask templates and SQLAlchemy ORM.

This project was a coursework I did for my COMP2011 module in University of Leeds. 

🔗[Visit the deployed application here](https://sworld-ha9e.onrender.com)

---

## 🚀 Features

- 🔐 **User Authentication** — Sign up, log in, and manage sessions securely using Flask-Login.  
- 📝 **Post Creation & Management** — Users can create, edit, and view posts.  
- ❤️ **Social Interactions** — Like and follow functionalities with relational database tracking.  
- 🔍 **Search Functionality** — Search users and explore trending posts.  
- 👤 **Profile Customization** — Change username, password, and display settings.  
- 🧭 **Explore Page** — View posts from other users and discover new content.  
- 🗂️ **Database Integration** — Powered by SQLite and SQLAlchemy ORM.  
- ⚙️ **Modular Structure** — Cleanly separated into configuration, models, routes, and forms.  

---

## 🧩 Project Structure

```

📂 sworld/
├── app/
│   ├── **init**.py          # Flask app initialization and configuration
│   ├── routes.py            # Application routes (views)
│   ├── models.py            # SQLAlchemy models (User, Post, Follow, Like)
│   ├── forms.py             # Flask-WTF forms for login, signup, and settings
│   ├── templates/           # HTML templates for pages
│   └── static/              # CSS, JS, and icon assets
│
├── config.py                # Configuration class (database URI, secret key)
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation

````

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/yourusername/sworld.git
cd sworld
````

### 2️⃣ Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # For macOS/Linux
venv\Scripts\activate         # For Windows
```

### 3️⃣ Install required dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Initialize the database

Run the following commands in the project root:

```bash
python
>>> from app import db, app
>>> with app.app_context():
...     db.create_all()
... 
exit()
```

Alternatively, just run:

```bash
python run.py
```

The database (`site.db`) will be created automatically.

---

## ▶️ Running the Application

To start the development server:

```bash
python run.py
```

The app will run locally at:
👉 **[http://127.0.0.1:5000/](http://127.0.0.1:5000/)**

Use `Ctrl + C` to stop the server.

---

## 🧰 Technologies Used

* **Python 3.x**
* **Flask**
* **Flask-SQLAlchemy**
* **Flask-WTF**
* **Flask-Login**
* **Flask-Migrate**
* **SQLite**
* **HTML / CSS / Jinja2**
* **JavaScript**

---

## 📸 Preview

You can view screenshots, design walkthroughs, and detailed function explanations in the full report below:

📄 [View Full Report (Report.pdf)](./Report.pdf)
