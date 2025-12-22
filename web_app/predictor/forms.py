from django import forms

class RegisterForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ім\'я'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    password = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
    )

class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    password = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
    )

class LoanForm(forms.Form):
    GENDER_CHOICES = [('Male', 'Чоловік'), ('Female', 'Жінка')]
    MARRIED_CHOICES = [('Yes', 'Так'), ('No', 'Ні')]
    EDUCATION_CHOICES = [('Graduate', 'З вищою освітою'), ('Not Graduate', 'Без вищої освіти')]
    SELF_EMPLOYED_CHOICES = [('Yes', 'Так'), ('No', 'Ні')]
    PROPERTY_AREA_CHOICES = [('Urban', 'Місто'), ('Rural', 'Село'), ('Semiurban', 'Передмістя')]
    DEPENDENTS_CHOICES = [('0', '0'), ('1', '1'), ('2', '2'), ('3', '3+')]
    CREDIT_HISTORY_CHOICES = [(1, 'Так'), (0, 'Ні')]
    
    Gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
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
    
    ApplicantIncome = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Дохід заявника'})
    )
    
    CoapplicantIncome = forms.FloatField(
        min_value=0,
        required=False,
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




