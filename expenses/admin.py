from django.contrib import admin
from .models import Category, Expense, Budget, RecurringExpense, Tag, Account, Currency

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'symbol', 'exchange_rate')
    search_fields = ('code', 'name')
    ordering = ('code',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'icon', 'color')
    list_filter = ('user',)
    search_fields = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    list_filter = ('user',)
    search_fields = ('name',)

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'initial_balance', 'current_balance', 'currency')
    list_filter = ('user', 'currency')
    search_fields = ('name',)

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount', 'currency', 'date', 'category', 'account', 'user')
    list_filter = ('date', 'category', 'user', 'currency')
    search_fields = ('description',)
    date_hierarchy = 'date'
    filter_horizontal = ('tags',)

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('category', 'amount', 'month', 'year', 'spent', 'remaining', 'percentage_used')
    list_filter = ('category__user', 'year', 'month')
    search_fields = ('category__name',)

@admin.register(RecurringExpense)
class RecurringExpenseAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount', 'currency', 'frequency', 'category', 'user', 'is_active')
    list_filter = ('frequency', 'category', 'user', 'is_active')
    search_fields = ('description',)
