# Library Management System API

This project is a RESTful API for managing a library system, built with Django and Django REST Framework (DRF). It allows for managing books, students, and issued books efficiently. The API supports issuing, returning, and renewing books while enforcing borrowing limits.

---

## Project Overview

The Library Management System includes the following functionalities:

- **Books**: Add, retrieve, update, and delete book records.
- **Students**: Register and manage student details, including borrowing limits.
- **Issued Books**: Issue books to students, renew issued books, and return books while maintaining borrowing records.

---

## Features

- Add and manage books in the library.
- Issue books to students with a limit of 3 active loans per student.
- Return books and update borrowing records.
- Renew books and calculate overdue fines (₹1/day for late returns).
- Check a book's current status (issued or available).

---

## Setup Instructions

### Prerequisites

Ensure the following are installed on your system:

- Python 3.x
- pip (Python package manager)
- Django
- Django REST Framework

### Steps to Run the Project

#### 1. Clone the Repository

```bash
git clone https://github.com/coder30247/library-management-api.git
cd library-management-api
```

2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install Dependencies
```bash
pip install -r requirements.txt
```
4. Run Migrations
```bash
python manage.py migrate
```
5. Create a Superuser
```bash
python manage.py createsuperuser
```
Follow the prompts to set up your admin credentials.

6. Start the Development Server
```bash
python manage.py runserver
```
Access the application at http://127.0.0.1:8000/.
## Database Models

### **Book\_Data**

| Field        | Type    | Description        |
| ------------ | ------- | ------------------ |
| book\_id     | Integer | Primary key        |
| book\_name   | String  | Name of the book   |
| author\_name | String  | Author of the book |

### **Student\_Data**

| Field                 | Type    | Description              |
| --------------------- | ------- | ------------------------ |
| register\_number      | Integer | Primary key              |
| student\_name         | String  | Name of the student      |
| student\_email        | String  | Email of the student     |
| due\_amount           | Decimal | Total overdue fines      |
| borrowed\_book\_count | Integer | Number of borrowed books |

### **Issued\_Book\_Data**

| Field        | Type      | Description                  |
| ------------ | --------- | ---------------------------- |
| id           | AutoField | Primary key                  |
| borrower     | FK        | Foreign key to Student\_Data |
| issued\_book | FK        | Foreign key to Book\_Data    |
| issue\_date  | Date      | Date of book issuance        |
| due\_date    | Date      | Due date for return          |

# API Endpoints

##Authentication
-**POST** `/api/token/`

Obtain a JWT token for authentication.
Request Body Example:
```json
{
  "username": "your_username",
  "password": "your_password"
}
```
Response Example:
```json
{
  "access": "your_access_token",
  "refresh": "your_refresh_token"
}
```
-**POST** `/api/token/refresh/`

Refresh an expired access token using the refresh token.
Request Body Example:
```json
{
  "refresh": "your_refresh_token"
}
```
Response Example:
```json
{
  "access": "new_access_token"
}
```
## Book Management

- **GET** `/book_data/`  
  Retrieve all books.

- **POST** `/book_data/add_book/`  
  Add a new book to the library.

- **GET** `/book_data/retrieve_book/<book_id>`  
  Retrieve a book.

- **PUT** `/book_data/update_book/<book_id>/`  
  Update book details.

- **DELETE** `/book_data/delete_book/<book_id>/`  
  Delete a book record.

---

## Student Management

- **GET** `/student_data/`  
  Retrieve all student records.
  
- **POST** `/student_data/add_student/`  
  Register a new student.
  
- **GET** `/student_data/retrieve_student/<register_number>/`  
  Retrieve a student record.

- **PUT** `/student_data/<register_number>/`  
  Update student details.

- **DELETE** `/student_data/<register_number>/`  
  Delete a student record.

---

## Issued Book Management

- **GET** `/issued_book_data/`  
  Get all the Issued book details.

- **POST** `/issued_book_data/issue_book/`  
  Issue a book to a student.

- **DELETE** `/issued_book_data/return_book/<book_id>/`  
  Return a book using its `book_id`.

- **GET** `/issued_book_data/retrieve_issued_book/<book_id>/`  
  Check if a book is issued or available.

- **PUT** `/issued_book_data/renew_issued_book/<book_id>/`  
  Renew an issued book and calculate overdue fines.

---

## Error Handling

- **400 Bad Request**: Invalid request data.
- **404 Not Found**: Resource not found (e.g., book or student).
- **500 Internal Server Error**: Unexpected server error.

---

## Additional Information

- **Django Version**: 5.1+
- **Django REST Framework Version**: 3.14+
- **Default Database**: SQLite (configurable in `settings.py`).

---

## Contributors

**coder30247**  
Feel free to contribute, report issues, or suggest improvements!
