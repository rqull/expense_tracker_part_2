from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.db.models import Sum, Count
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.utils import timezone
from .models import Category, Expense, Budget, RecurringExpense, Tag, Account, Currency
from .forms import (
    UserRegistrationForm, CategoryForm, ExpenseForm, BudgetForm, 
    RecurringExpenseForm, TagForm, AccountForm, ExpenseFilterForm
)
import csv
import datetime
import json

# Authentication views
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create default category for the user
            Category.objects.create(name='General', user=user, color='#3498db')
            # Create default account
            default_currency = Currency.objects.first()
            if not default_currency:
                default_currency = Currency.objects.create(
                    code='IDR',
                    name='Indonesian Rupiah',
                    symbol='Rp',
                    exchange_rate=1.0
                )
            Account.objects.create(name='Cash', user=user, currency=default_currency)
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

# Dashboard views
@login_required
def dashboard(request):
    today = timezone.now().date()
    current_month = today.month
    current_year = today.year

    # Get recent expenses
    recent_expenses = Expense.objects.filter(
        user=request.user
    ).order_by('-date', '-created_at')[:5]

    # Get month's total expenses
    month_expenses = Expense.objects.filter(
        user=request.user,
        date__month=current_month,
        date__year=current_year
    ).aggregate(total=Sum('amount'))['total'] or 0

    # Get budgets and their usage
    budgets = Budget.objects.filter(
        category__user=request.user,
        month=current_month,
        year=current_year
    )

    # Get expense data for chart (last 6 months)
    months_data = []
    categories_data = []

    # Last 6 months data
    for i in range(5, -1, -1):
        date = today - datetime.timedelta(days=30 * i)
        month_name = date.strftime('%b %Y')
        month_total = Expense.objects.filter(
            user=request.user,
            date__month=date.month,
            date__year=date.year
        ).aggregate(total=Sum('amount'))['total'] or 0
        months_data.append({'month': month_name, 'amount': float(month_total)})

    # Category data
    categories = Category.objects.filter(user=request.user)
    for category in categories:
        amount = Expense.objects.filter(
            user=request.user,
            category=category,
            date__month=current_month,
            date__year=current_year
        ).aggregate(total=Sum('amount'))['total'] or 0
        if amount > 0:  # Only include categories with expenses
            categories_data.append({'category': category.name, 'amount': float(amount), 'color': category.color})

    context = {
        'recent_expenses': recent_expenses,
        'month_expenses': month_expenses,
        'budgets': budgets,
        'months_data': json.dumps(months_data),
        'categories_data': json.dumps(categories_data),
    }
    return render(request, 'expenses/dashboard.html', context)

# Expense views
@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date', '-created_at')
    filter_form = ExpenseFilterForm(user=request.user, data=request.GET or None)

    if filter_form.is_valid():
        if filter_form.cleaned_data.get('category'):
            expenses = expenses.filter(category=filter_form.cleaned_data['category'])
        if filter_form.cleaned_data.get('date_from'):
            expenses = expenses.filter(date__gte=filter_form.cleaned_data['date_from'])
        if filter_form.cleaned_data.get('date_to'):
            expenses = expenses.filter(date__lte=filter_form.cleaned_data['date_to'])
        if filter_form.cleaned_data.get('amount_min'):
            expenses = expenses.filter(amount__gte=filter_form.cleaned_data['amount_min'])
        if filter_form.cleaned_data.get('amount_max'):
            expenses = expenses.filter(amount__lte=filter_form.cleaned_data['amount_max'])
        if filter_form.cleaned_data.get('description'):
            expenses = expenses.filter(description__icontains=filter_form.cleaned_data['description'])
        if filter_form.cleaned_data.get('tags'):
            expenses = expenses.filter(tags__in=filter_form.cleaned_data['tags']).distinct()

    # Calculate total amount
    total_amount = expenses.aggregate(total=Sum('amount'))['total'] or 0

    return render(request, 'expenses/expense_list.html', {
        'expenses': expenses,
        'filter_form': filter_form,
        'total_amount': total_amount
    })

@login_required
def expense_create(request):
    if request.method == 'POST':
        form = ExpenseForm(request.user, request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            # Many to Many relationships
            form.save_m2m()
            messages.success(request, 'Expense added successfully!')
            return redirect('expense_list')
    else:
        form = ExpenseForm(request.user)

    return render(request, 'expenses/expense_form.html', {
        'form': form,
        'title': 'Add Expense'
    })

@login_required
def expense_update(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)

    if request.method == 'POST':
        form = ExpenseForm(request.user, request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense updated successfully!')
            return redirect('expense_list')
    else:
        form = ExpenseForm(request.user, instance=expense)

    return render(request, 'expenses/expense_form.html', {
        'form': form,
        'expense': expense,
        'title': 'Edit Expense'
    })

@login_required
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)

    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Expense deleted successfully!')
        return redirect('expense_list')

    return render(request, 'expenses/expense_confirm_delete.html', {'expense': expense})

@login_required
def export_expenses_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="expenses.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Amount', 'Currency', 'Description', 'Category', 'Account', 'Tags'])

    expenses = Expense.objects.filter(user=request.user).order_by('date')
    for expense in expenses:
        tags = ", ".join([tag.name for tag in expense.tags.all()])
        account_name = expense.account.name if expense.account else 'N/A'
        writer.writerow([
            expense.date, 
            expense.amount, 
            expense.currency.code,
            expense.description, 
            expense.category.name, 
            account_name,
            tags
        ])

    return response

# Category views
class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'expenses/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'expenses/category_form.html'
    success_url = reverse_lazy('category_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Category created successfully!')
        return super().form_valid(form)

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'expenses/category_form.html'
    success_url = reverse_lazy('category_list')

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Category updated successfully!')
        return super().form_valid(form)

class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'expenses/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Category deleted successfully!')
        return super().delete(request, *args, **kwargs)

# Budget views
class BudgetListView(LoginRequiredMixin, ListView):
    model = Budget
    template_name = 'expenses/budget_list.html'
    context_object_name = 'budgets'

    def get_queryset(self):
        return Budget.objects.filter(category__user=self.request.user)

class BudgetCreateView(LoginRequiredMixin, CreateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'expenses/budget_form.html'
    success_url = reverse_lazy('budget_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Budget created successfully!')
        return super().form_valid(form)

class BudgetUpdateView(LoginRequiredMixin, UpdateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'expenses/budget_form.html'
    success_url = reverse_lazy('budget_list')

    def get_queryset(self):
        return Budget.objects.filter(category__user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Budget updated successfully!')
        return super().form_valid(form)

class BudgetDeleteView(LoginRequiredMixin, DeleteView):
    model = Budget
    template_name = 'expenses/budget_confirm_delete.html'
    success_url = reverse_lazy('budget_list')

    def get_queryset(self):
        return Budget.objects.filter(category__user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Budget deleted successfully!')
        return super().delete(request, *args, **kwargs)

# Account views
class AccountListView(LoginRequiredMixin, ListView):
    model = Account
    template_name = 'expenses/account_list.html'
    context_object_name = 'accounts'

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)

class AccountCreateView(LoginRequiredMixin, CreateView):
    model = Account
    form_class = AccountForm
    template_name = 'expenses/account_form.html'
    success_url = reverse_lazy('account_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.current_balance = form.instance.initial_balance
        messages.success(self.request, 'Account created successfully!')
        return super().form_valid(form)

class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = Account
    form_class = AccountForm
    template_name = 'expenses/account_form.html'
    success_url = reverse_lazy('account_list')

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)

    def form_valid(self, form):
        # Update current balance based on the difference in initial balance
        old_initial = self.get_object().initial_balance
        new_initial = form.instance.initial_balance
        form.instance.current_balance += (new_initial - old_initial)

        messages.success(self.request, 'Account updated successfully!')
        return super().form_valid(form)

class AccountDeleteView(LoginRequiredMixin, DeleteView):
    model = Account
    template_name = 'expenses/account_confirm_delete.html'
    success_url = reverse_lazy('account_list')

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Account deleted successfully!')
        return super().delete(request, *args, **kwargs)

# Recurring Expense views
class RecurringExpenseListView(LoginRequiredMixin, ListView):
    model = RecurringExpense
    template_name = 'expenses/recurring_expense_list.html'
    context_object_name = 'recurring_expenses'

    def get_queryset(self):
        return RecurringExpense.objects.filter(user=self.request.user)

class RecurringExpenseCreateView(LoginRequiredMixin, CreateView):
    model = RecurringExpense
    form_class = RecurringExpenseForm
    template_name = 'expenses/recurring_expense_form.html'
    success_url = reverse_lazy('recurring_expense_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Recurring expense created successfully!')
        return super().form_valid(form)

class RecurringExpenseUpdateView(LoginRequiredMixin, UpdateView):
    model = RecurringExpense
    form_class = RecurringExpenseForm
    template_name = 'expenses/recurring_expense_form.html'
    success_url = reverse_lazy('recurring_expense_list')

    def get_queryset(self):
        return RecurringExpense.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Recurring expense updated successfully!')
        return super().form_valid(form)

class RecurringExpenseDeleteView(LoginRequiredMixin, DeleteView):
    model = RecurringExpense
    template_name = 'expenses/recurring_expense_confirm_delete.html'
    success_url = reverse_lazy('recurring_expense_list')

    def get_queryset(self):
        return RecurringExpense.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Recurring expense deleted successfully!')
        return super().delete(request, *args, **kwargs)

# Tag views
class TagListView(LoginRequiredMixin, ListView):
    model = Tag
    template_name = 'expenses/tag_list.html'
    context_object_name = 'tags'

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user)

class TagCreateView(LoginRequiredMixin, CreateView):
    model = Tag
    form_class = TagForm
    template_name = 'expenses/tag_form.html'
    success_url = reverse_lazy('tag_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Tag created successfully!')
        return super().form_valid(form)

class TagUpdateView(LoginRequiredMixin, UpdateView):
    model = Tag
    form_class = TagForm
    template_name = 'expenses/tag_form.html'
    success_url = reverse_lazy('tag_list')

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Tag updated successfully!')
        return super().form_valid(form)

class TagDeleteView(LoginRequiredMixin, DeleteView):
    model = Tag
    template_name = 'expenses/tag_confirm_delete.html'
    success_url = reverse_lazy('tag_list')

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Tag deleted successfully!')
        return super().delete(request, *args, **kwargs)
