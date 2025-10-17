# final-project-djangorest
# Recipe App

A Django REST Framework application for managing categorized recipes with user authentication, password recovery, and email verification.

## Features

### User Authentication
- Register, login, and logout
- Password recovery using recovery questions
- Email verification on registration

### Recipe Management
- Create, read, update, and delete own recipes and categories
- Read recipes by all the other users
- Categorize recipes

### User Profiles
- Access and modify own profile info

### Admin Interface
- Admin can manage users and recipes via Django Admin

### Testing
- Unit tests for user and recipes apps included

## Installation

### Clone the repository:
```bash
git clone <repo-url>
cd final-project-djangorest/
```

### Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

### Install dependencies:
```bash
pip install -r requirements.txt
```

### Create a .env file 
Based on .env.example, create a .env file and add your SMTP credentials from your Brevo account to enable email verification.  
**Note**: If the .env file has already been provided to you personally by me, you may use that directly.

### Run migrations:
```bash
python manage.py migrate
```

### Create a superuser:
(for admin access)
```bash
python manage.py createsuperuser
```

### Start the development server:
```bash
python manage.py runserver
```

## Usage

### Register a new user  
POST /api/register/  
JSON:
```json
{
    "username": "alice",
    "email": "alice@example.com",
    "password": "Alice123!",
    "password2": "Alice123!",
    "recovery_question": "Favorite color?",
    "recovery_answer": "Blue",
    "age": 20,
    "profile_pic": null
}
```

### Email Verification  
After registration, an email will be sent with a verification link. Click it to activate the account.

### Login after verification
POST /api/login/ with username and password as JSON:
```json
{
    "username": "alice",
    "password": "Alice123!"
}
```

## Refresh Token
POST /api/token/refresh/ with refresh token → get new access token

### Password Recovery  
POST /api/recovery-question/ with username → get recovery_question and token
```json
{
    "username": "alice"
}
```

POST /api/reset-password/ with token, recovery_answer, new_password, confirm_password → reset password
```json
{
    "token": <token>,
    "recovery_answer": "Blue",
    "new_password": "newpass123",
    "confirm_password": "newpass123"
}
```

### User Info
GET /api/me/ → get user info

PUT /api/me/ → update user info

DELETE /api/me/ → delete user

(Requires authentication.)

### Recipe CRUD  
GET /api/recipes/ → list all recipes

GET /api/recipes/my/ → list own recipes

POST /api/recipes/my/ → create new recipe

PUT /api/recipes/{id}/ → update a recipe

DELETE /api/recipes/{id}/ → delete a recipe

(All recipe endpoints require authentication.)


### Category CRUD  
GET /api/categories/ → list all categories

GET /api/categories/my/ → list own categories

POST /api/categories/my/ → create new category

PUT /api/categories/{id}/ → update a category

DELETE /api/categories/{id}/ → delete a category

(All category endpoints require authentication.)

### View Categorized Recipes
GET /api/recipes/category/{category_id}/ → view all the recipes by all the users under that category

(Requires authentication)

### Logout 
POST /api/logout/ → with refresh token

(Requires authentication)

## Tests  
Run tests for both apps:

```bash
python manage.py test user
```
```bash
python manage.py test recipes
```

## Docker (Optional)  
Build and run the Docker container:

```bash
docker build -t recipe-app .
docker run -p 8000:8000 recipe-app
```

## Notes
Media files and the SQLite database are excluded from GitHub.