# Expense Tracker

A full-stack Django application for tracking personal expenses, with features for budgeting, recurring expenses, and multi-currency support.

## Features

- User authentication (register, login, password reset)
- Expense tracking with categories, tags, and accounts
- Budget management with progress visualization
- Recurring expenses for subscriptions and regular bills
- Multi-currency support
- Data visualization with charts
- Export data to CSV
- Mobile-responsive interface
- Django Admin integration
- Environment variables using python-dotenv

## Tech Stack

- **Backend**: Django
- **Database**: PostgreSQL
- **Frontend**: Tailwind CSS, Alpine.js, HTMX
- **Charts**: Chart.js
- **Icons**: Font Awesome
- **Environment**: python-dotenv

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL
- pip

### Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd expense-tracker
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory:
   ```
   # Django Settings
   DEBUG=True
   SECRET_KEY=your-secret-key-here

   # Database Settings
   DB_NAME=YOUR DATABASE NAME
   DB_USER=YOUR DATABASE USER
   DB_PASSWORD=YOUR DATABASE PASSWORD
   DB_HOST=YOUR HOST
   DB_PORT=YOUR PORT
   ```

5. Configure your database in `settings.py`:
   ```python
   from dotenv import load_dotenv
   import os

   load_dotenv()

   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': os.getenv('DB_NAME'),
           'USER': os.getenv('DB_USER'),
           'PASSWORD': os.getenv('DB_PASSWORD'),
           'HOST': os.getenv('DB_HOST'),
           'PORT': os.getenv('DB_PORT'),
       }
   }
   ```

6. Run migrations:
   ```
   python manage.py makemigrations expenses
   python manage.py migrate
   ```

7. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

8. Load initial data (currencies):
   ```
   python manage.py loaddata currencies
   ```

9. Start the development server:
   ```
   python manage.py runserver
   ```

10. Visit `http://127.0.0.1:8000/` in your browser

## Usage

1. Register a new account or login
2. Add categories for your expenses
3. Set up monthly budgets for your categories
4. Add your expenses
5. View your spending patterns in the dashboard

## Important Notes

- Never commit your `.env` file to version control
- Keep your SECRET_KEY secure and unique for each deployment

## License

This project is licensed under the MIT License.
