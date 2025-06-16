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

## Tech Stack

- **Backend**: Django
- **Database**: PostgreSQL
- **Frontend**: Tailwind CSS, Alpine.js, HTMX
- **Charts**: Chart.js
- **Icons**: Font Awesome

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

4. Configure your database in `settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'expense_tracker_db',
           'USER': 'postgres',
           'PASSWORD': '12345',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

5. Run migrations:
   ```
   python manage.py makemigrations expenses
   python manage.py migrate
   ```

6. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

7. Load initial data (currencies):
   ```
   python manage.py loaddata currencies
   ```

8. Start the development server:
   ```
   python manage.py runserver
   ```

9. Visit `http://127.0.0.1:8000/` in your browser

## Usage

1. Register a new account or login
2. Add categories for your expenses
3. Set up monthly budgets for your categories
4. Add your expenses
5. View your spending patterns in the dashboard

## License

This project is licensed under the MIT License.
