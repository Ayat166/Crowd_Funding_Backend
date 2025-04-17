# Crowd-Funding Web App (Backend)

## Project Overview
This is the backend for the Crowd-Funding web application, built using **Django** and **Django REST Framework** (DRF). The project provides RESTful APIs for authentication, project creation, donations, and user management.

## Technologies Used
- **Django** (Backend Framework)
- **Django REST Framework (DRF)** (API Development)
- **SQLite** (Default Database, can be changed to PostgreSQL/MySQL)

## Features Implemented
1. **User Authentication**
   - User registration with email verification
   - User login/logout
   - User profile management
   
2. **Project Management**
   - Users can create, view, update, and delete projects
   - Projects have titles, descriptions, images, target amounts, and categories
   
3. **Example of API Endpoints** (Implemented Using APIView, Not Routers)
   - `/api/users/` → List and create users
   - `/api/users/<user_id>/` → Retrieve, update, delete a user
   - `/api/projects/` → List and create projects
   - `/api/projects/<project_id>/` → Retrieve, update, delete a project

## Getting Started

### 1. Clone the Repository
```sh
  git clone https://github.com/Ayat166/Crowd_Funding_Backend.git
  cd crowdfunding-backend
```

### 2. Create a Virtual Environment
```sh
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```sh
  pip install -r requirements.txt
```

### 4. Apply Database Migrations
```sh
  python manage.py makemigrations
  python manage.py migrate
```

### 5. Run the Development Server
```sh
  python manage.py runserver
```
The API will be available at `http://127.0.0.1:8000/`

Happy Coding! 🚀

