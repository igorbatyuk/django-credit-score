# імпортуємо forms з Django - для створення форм
from django import forms

# форма для реєстрації нового користувача
# Form - базовий клас Django для форм
class RegisterForm(forms.Form):
    # CharField - поле для введення тексту
    username = forms.CharField(
        max_length=50,  # максимальна довжина
        # widget визначає як поле буде відображатися в HTML
        # attrs - атрибути HTML елемента (class для Bootstrap стилів, placeholder для підказки)
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ім\'я користувача'})
    )
    password = forms.CharField(
        max_length=100,
        # PasswordInput приховує введений текст (показує крапки)
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
    )
    email = forms.EmailField(
        required=False,  # поле необов'язкове
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email (необов\'язково)'})
    )

# форма для входу користувача
class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ім\'я користувача'})
    )
    password = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
    )

# форма для введення даних про займ (основна форма проєкту)
class LoanForm(forms.Form):
    # визначаємо варіанти вибору для кожного поля
    # формат: (значення_для_моделі, текст_для_користувача)
    GENDER_CHOICES = [('Male', 'Чоловік'), ('Female', 'Жінка')]
    MARRIED_CHOICES = [('Yes', 'Так'), ('No', 'Ні')]
    EDUCATION_CHOICES = [('Graduate', 'З вищою освітою'), ('Not Graduate', 'Без вищої освіти')]
    SELF_EMPLOYED_CHOICES = [('Yes', 'Так'), ('No', 'Ні')]
    PROPERTY_AREA_CHOICES = [('Urban', 'Місто'), ('Rural', 'Село'), ('Semiurban', 'Передмістя')]
    DEPENDENTS_CHOICES = [('0', '0'), ('1', '1'), ('2', '2'), ('3', '3+')]  # '3+' означає 3 або більше
    CREDIT_HISTORY_CHOICES = [(1, 'Так'), (0, 'Ні')]  # 1 = так, 0 = ні
    
    # ChoiceField - поле з вибором зі списку (випадаючий список)
    Gender = forms.ChoiceField(
        choices=GENDER_CHOICES,  # варіанти вибору
        widget=forms.Select(attrs={'class': 'form-control'})  # Select - випадаючий список
    )
    Married = forms.ChoiceField(
        choices=MARRIED_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    Dependents = forms.ChoiceField(
        choices=DEPENDENTS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    Education = forms.ChoiceField(
        choices=EDUCATION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    Self_Employed = forms.ChoiceField(
        choices=SELF_EMPLOYED_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    # IntegerField - поле для цілих чисел
    ApplicantIncome = forms.IntegerField(
        min_value=0,  # мінімальне значення (не може бути від'ємним)
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Дохід заявника'})
    )
    
    # FloatField - поле для десяткових чисел
    CoapplicantIncome = forms.FloatField(
        min_value=0,
        required=False,  # поле необов'язкове (може бути порожнім)
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Дохід співзаявника (0 якщо немає)'})
    )
    LoanAmount = forms.FloatField(
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Сума займу'})
    )
    Loan_Amount_Term = forms.FloatField(
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Термін займу (в днях)'})
    )
    Credit_History = forms.ChoiceField(
        choices=CREDIT_HISTORY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    Property_Area = forms.ChoiceField(
        choices=PROPERTY_AREA_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )




