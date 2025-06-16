from django.core.management.base import BaseCommand
from django.utils import timezone
from expenses.models import RecurringExpense, Expense
from datetime import timedelta, date
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Generate expenses from recurring expense definitions'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        recurring_expenses = RecurringExpense.objects.filter(is_active=True)
        generated_count = 0

        for recurring in recurring_expenses:
            # Skip if end date is set and has passed
            if recurring.end_date and recurring.end_date < today:
                continue

            # Skip if no last generated date and start date is in the future
            if not recurring.last_generated and recurring.start_date > today:
                continue

            last_date = recurring.last_generated or recurring.start_date
            next_date = self.calculate_next_date(last_date, recurring.frequency)

            # Generate all expenses up to today
            while next_date <= today:
                # Create the expense
                Expense.objects.create(
                    user=recurring.user,
                    amount=recurring.amount,
                    date=next_date,
                    description=recurring.description,
                    category=recurring.category,
                    account=recurring.account,
                    currency=recurring.currency
                )
                generated_count += 1

                # Update the recurring expense's last_generated date
                recurring.last_generated = next_date
                recurring.save()

                # Calculate the next date
                next_date = self.calculate_next_date(next_date, recurring.frequency)

                # Break if we've hit the end date
                if recurring.end_date and next_date > recurring.end_date:
                    break

        self.stdout.write(
            self.style.SUCCESS(f'Successfully generated {generated_count} expenses from recurring expenses')
        )

    def calculate_next_date(self, last_date, frequency):
        if frequency == 'daily':
            return last_date + timedelta(days=1)
        elif frequency == 'weekly':
            return last_date + timedelta(weeks=1)
        elif frequency == 'monthly':
            # Handle month rollover
            year = last_date.year
            month = last_date.month + 1
            if month > 12:
                month = 1
                year += 1
            day = min(last_date.day, self.get_days_in_month(year, month))
            return date(year, month, day)
        elif frequency == 'yearly':
            # Handle leap years
            year = last_date.year + 1
            month = last_date.month
            day = min(last_date.day, self.get_days_in_month(year, month))
            return date(year, month, day)
        else:
            raise ValueError(f'Unknown frequency: {frequency}')

    def get_days_in_month(self, year, month):
        if month == 2:  # February
            if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):  # Leap year
                return 29
            else:
                return 28
        elif month in [4, 6, 9, 11]:  # April, June, September, November
            return 30
        else:
            return 31
