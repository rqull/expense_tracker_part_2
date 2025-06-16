from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Sum
from datetime import datetime

class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=5)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4, help_text='Exchange rate to IDR (Indonesian Rupiah)')

    def __str__(self):
        return f"{self.code} - {self.name} ({self.symbol})"

    class Meta:
        verbose_name_plural = 'Currencies'

class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    icon = models.CharField(max_length=50, blank=True, null=True, help_text='CSS class for icon (e.g., fa-food)')
    color = models.CharField(max_length=20, default='#3498db', help_text='Color for category visualization')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'
        unique_together = ['name', 'user']

    def total_expenses(self, year=None, month=None):
        queryset = self.expense_set.all()
        if year:
            queryset = queryset.filter(date__year=year)
        if month:
            queryset = queryset.filter(date__month=month)
        return queryset.aggregate(Sum('amount'))['amount__sum'] or 0

    def get_budget(self, year=None, month=None):
        if not year:
            year = datetime.now().year
        if not month:
            month = datetime.now().month

        try:
            budget = Budget.objects.get(category=self, year=year, month=month)
            return budget.amount
        except Budget.DoesNotExist:
            return 0

class Tag(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ['name', 'user']

class Account(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    initial_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    current_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, default=1)  # Default to IDR

    def __str__(self):
        return self.name

    def update_balance(self):
        expenses_sum = Expense.objects.filter(account=self).aggregate(Sum('amount'))['amount__sum'] or 0
        self.current_balance = self.initial_balance - expenses_sum
        self.save()

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    description = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, default=1)  # Default to IDR
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.description} - {self.amount} {self.currency.symbol} ({self.date})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.account:
            self.account.update_balance()

class Budget(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    year = models.IntegerField()
    month = models.IntegerField()

    def __str__(self):
        return f"{self.category.name} - {self.amount} ({self.month}/{self.year})"

    class Meta:
        unique_together = ['category', 'year', 'month']

    def clean(self):
        if self.month < 1 or self.month > 12:
            raise ValidationError({'month': 'Month must be between 1 and 12'})

    def spent(self):
        return self.category.total_expenses(year=self.year, month=self.month)

    def remaining(self):
        return self.amount - self.spent()

    def percentage_used(self):
        if self.amount == 0:
            return 100
        return min(100, int((self.spent() / self.amount) * 100))

class RecurringExpense(models.Model):
    FREQUENCY_CHOICES = (
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    last_generated = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, default=1)  # Default to IDR

    def __str__(self):
        return f"{self.description} - {self.amount} {self.currency.symbol} ({self.frequency})"
