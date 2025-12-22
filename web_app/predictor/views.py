from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from .forms import RegisterForm, LoginForm, LoanForm
import pickle
import pandas as pd
import os
import warnings
from django.conf import settings

warnings.filterwarnings('ignore', category=UserWarning, module='sklearn')

BASE_DIR_STR = str(settings.BASE_DIR)
PROJECT_ROOT = os.path.dirname(BASE_DIR_STR)
MODEL_PATH = os.path.join(PROJECT_ROOT, 'data_science', 'loan_model.pkl')
FEATURE_COLUMNS_PATH = os.path.join(PROJECT_ROOT, 'data_science', 'feature_columns.pkl')

try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    model = None

try:
    with open(FEATURE_COLUMNS_PATH, 'rb') as f:
        feature_columns = pickle.load(f)
except FileNotFoundError:
    feature_columns = None

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Користувач з таким email вже існує!')
                return render(request, 'register.html', {'form': form})
            
            user = User.objects.create(
                name=name,
                email=email,
                password=password
            )
            messages.success(request, 'Реєстрація успішна! Тепер ви можете увійти.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            try:
                user = User.objects.get(email=email, password=password)
                request.session['user_id'] = user.id
                request.session['name'] = user.name
                messages.success(request, f'Вітаємо, {user.name}!')
                return redirect('predict')
            except User.DoesNotExist:
                messages.error(request, 'Невірний email або пароль!')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    request.session.flush()
    messages.success(request, 'Ви вийшли з системи.')
    return redirect('login')

def predict(request):
    if 'user_id' not in request.session:
        messages.warning(request, 'Будь ласка, увійдіть в систему.')
        return redirect('login')
    
    if model is None:
        messages.error(request, 'Модель не завантажена!')
        return render(request, 'loan_form.html', {'form': LoanForm()})
    
    if feature_columns is None:
        messages.error(request, 'Список стовпців не завантажено!')
        return render(request, 'loan_form.html', {'form': LoanForm()})
    
    if request.method == 'POST':
        form = LoanForm(request.POST)
        
        if form.is_valid():
            data = form.cleaned_data.copy()
            
            if data['Dependents'] == '3':
                data['Dependents'] = 3
            else:
                data['Dependents'] = int(data['Dependents'])
            
            data['Credit_History'] = int(data['Credit_History'])
            
            if data.get('CoapplicantIncome') is None or data['CoapplicantIncome'] == '':
                data['CoapplicantIncome'] = 0.0
            else:
                data['CoapplicantIncome'] = float(data['CoapplicantIncome'])
            
            if feature_columns and model:
                row_data = []
                for col in feature_columns:
                    if col in data:
                        value = data[col]
                        if col in ['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term']:
                            try:
                                row_data.append(float(value))
                            except (ValueError, TypeError):
                                row_data.append(0.0)
                        elif col in ['Dependents', 'Credit_History']:
                            try:
                                row_data.append(int(value))
                            except (ValueError, TypeError):
                                row_data.append(0)
                        else:
                            row_data.append(str(value))
                    else:
                        if col in ['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term']:
                            row_data.append(0.0)
                        elif col in ['Dependents', 'Credit_History']:
                            row_data.append(0)
                        else:
                            row_data.append('')
                
                df = pd.DataFrame([row_data], columns=feature_columns)
                
                numeric_cols = ['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term']
                int_cols = ['Dependents', 'Credit_History']
                
                for col in numeric_cols:
                    if col in df.columns:
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0).astype(float)
                
                for col in int_cols:
                    if col in df.columns:
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
                
                for col in df.columns:
                    if col not in numeric_cols and col not in int_cols:
                        df[col] = df[col].astype(str)
            else:
                df = pd.DataFrame([data])
            
            try:
                if not isinstance(df, pd.DataFrame):
                    raise ValueError(f"df має бути DataFrame, а не {type(df)}")
                
                if df.shape[0] != 1:
                    raise ValueError(f"df має мати 1 рядок, але має {df.shape[0]}")
                
                if df.empty:
                    raise ValueError("DataFrame порожній")
                
                prediction = model.predict(df)[0]
                probability = model.predict_proba(df)[0]
                
                classes = model.classes_
                
                y_idx = None
                n_idx = None
                for i, cls in enumerate(classes):
                    if cls == 'Y':
                        y_idx = i
                    elif cls == 'N':
                        n_idx = i
                
                if y_idx is None or n_idx is None:
                    y_idx = 1
                    n_idx = 0
                
                prob_approved = probability[y_idx] * 100
                prob_rejected = probability[n_idx] * 100
                
                result = {
                    'prediction': 'Схвалено' if prediction == 'Y' else 'Відхилено',
                    'probability_approved': round(prob_approved, 2),
                    'probability_rejected': round(prob_rejected, 2),
                    'input_data': data
                }
                
                return render(request, 'result.html', {'result': result})
            except Exception as e:
                import traceback
                error_msg = f'Помилка при передбаченні: {str(e)}'
                print(f"Помилка при передбаченні: {error_msg}")
                print(traceback.format_exc())
                messages.error(request, error_msg)
                return render(request, 'loan_form.html', {'form': form})
        else:
            messages.error(request, 'Будь ласка, виправте помилки у формі.')
    else:
        form = LoanForm()
    
    return render(request, 'loan_form.html', {'form': form})
