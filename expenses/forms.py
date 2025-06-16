from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from .models import Category, Expense, Budget, RecurringExpense, Tag, Account
from datetime import datetime

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'icon', 'color']
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'}),
        }

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'date', 'description', 'category', 'account', 'tags', 'currency']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'value': datetime.now().strftime('%Y-%m-%d')}),
            'description': forms.TextInput(attrs={'placeholder': 'What did you spend on?'}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user=user)
        self.fields['account'].queryset = Account.objects.filter(user=user)
        self.fields['tags'].queryset = Tag.objects.filter(user=user)

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'amount', 'year', 'month']
        widgets = {
            'year': forms.NumberInput(attrs={'min': 2020, 'max': 2050}),
            'month': forms.NumberInput(attrs={'min': 1, 'max': 12}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user=user)
        # Set default values for year and month
        if not self.instance.pk:  # Only for new instances
            now = datetime.now()
            self.initial['year'] = now.year
            self.initial['month'] = now.month

class RecurringExpenseForm(forms.ModelForm):
    class Meta:
        model = RecurringExpense
        fields = ['amount', 'description', 'category', 'account', 'frequency', 'start_date', 'end_date', 'currency', 'is_active']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user=user)
        self.fields['account'].queryset = Account.objects.filter(user=user)

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'initial_balance', 'currency']

class ExpenseFilterForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.none(), required=False)
    date_from = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    date_to = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    amount_min = forms.DecimalField(required=False)
    amount_max = forms.DecimalField(required=False)
    description = forms.CharField(required=False)
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.none(), required=False)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user=user)
        self.fields['tags'].queryset = Tag.objects.filter(user=user)
