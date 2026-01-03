# Flask Todo App 📝

This is my first Flask backend project, built to practice full CRUD operations and backend concepts.

## 🚀 Features
- Add, edit, delete todos
- Mark todos as done / undo
- Separate active and completed tasks
- Group tasks by date
- PostgreSQL database
- Clean and simple UI

## 🛠 Tech Stack
- Python
- Flask
- PostgreSQL
- HTML, CSS
- psycopg2

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/Tshepang-Programmer/flask-todo-app.git
cd flask-todo-app

### 2. Clone the repository
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate

### 3 Install dependencies 
pip install -r requirements.txt

### 3 Install dependencies 
Create a .env file:
DB_NAME=Flask_Todo
DB_HOST=localhost
DB_USER=youruser
DB_PASSWORD=yourpassword
DB_PORT=5432

###5. Initialize database
python innit_db.py

###6. Run the app
python app.py
