# імпортуємо необхідні бібліотеки
from django.shortcuts import render, redirect  # для відображення сторінок та перенаправлення
from django.contrib import messages  # для показу повідомлень користувачу
from .models import User  # наша модель користувача
from .forms import RegisterForm, LoginForm, LoanForm  # форми для реєстрації, входу та займу
import pickle  # для завантаження збереженої моделі машинного навчання
import pandas as pd  # для роботи з даними у вигляді таблиць (DataFrame)
import os  # для роботи з файловою системою
import warnings  # щоб приховати попередження
from django.conf import settings  # налаштування Django

# приховати попередження про версії scikit-learn (щоб не засмічувати консоль)
warnings.filterwarnings('ignore', category=UserWarning, module='sklearn')

# тут завантажуємо модель машинного навчання при старті сервера
# BASE_DIR - це папка web_app, а модель лежить в data_science, тому треба піднятися на рівень вище
BASE_DIR_STR = str(settings.BASE_DIR)  # отримуємо шлях до папки web_app
PROJECT_ROOT = os.path.dirname(BASE_DIR_STR)  # піднімаємося на рівень вище (до папки 16)
MODEL_PATH = os.path.join(PROJECT_ROOT, 'data_science', 'loan_model.pkl')  # шлях до файлу моделі
FEATURE_COLUMNS_PATH = os.path.join(PROJECT_ROOT, 'data_science', 'feature_columns.pkl')  # шлях до списку стовпців

# пробуємо завантажити модель з файлу
# використовуємо try/except щоб не було помилки якщо файл не знайдено
try:
    with open(MODEL_PATH, 'rb') as f:  # 'rb' означає read binary (читати в бінарному режимі)
        model = pickle.load(f)  # завантажуємо модель
except FileNotFoundError:
    model = None  # якщо файл не знайдено, модель буде None

# пробуємо завантажити список стовпців (потрібен щоб знати в якому порядку передавати дані в модель)
try:
    with open(FEATURE_COLUMNS_PATH, 'rb') as f:
        feature_columns = pickle.load(f)
except FileNotFoundError:
    feature_columns = None

# функція для реєстрації нового користувача
def register(request):
    # перевіряємо чи це POST запит (користувач відправив форму)
    if request.method == 'POST':
        form = RegisterForm(request.POST)  # створюємо форму з даними які прийшли
        if form.is_valid():  # перевіряємо чи форма валідна (всі поля заповнені правильно)
            # отримуємо дані з форми
            name = form.cleaned_data['name']  # cleaned_data - це вже перевірені та очищені дані
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # перевіряємо чи вже існує користувач з таким email
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Користувач з таким email вже існує!')
                return render(request, 'register.html', {'form': form})
            
            # якщо все ок, створюємо нового користувача в базі даних
            # увага: пароль не хешується, бо це навчальний проєкт (в реальному проєкті треба хешувати!)
            user = User.objects.create(
                name=name,
                email=email,
                password=password
            )
            messages.success(request, 'Реєстрація успішна! Тепер ви можете увійти.')
            return redirect('login')  # перенаправляємо на сторінку входу
    else:
        # якщо це GET запит (просто відкрили сторінку), показуємо порожню форму
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})  # показуємо HTML сторінку з формою

# функція для входу користувача
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # пробуємо знайти користувача в базі даних
            try:
                user = User.objects.get(email=email, password=password)
                # якщо знайшли, зберігаємо інформацію про користувача в сесії
                # сесія - це спосіб зберігати дані між запитами (як cookies)
                request.session['user_id'] = user.id  # зберігаємо ID користувача
                request.session['name'] = user.name  # зберігаємо ім'я
                messages.success(request, f'Вітаємо, {user.name}!')
                return redirect('predict')  # перенаправляємо на сторінку передбачення
            except User.DoesNotExist:
                # якщо користувача не знайдено, показуємо помилку
                messages.error(request, 'Невірний email або пароль!')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# функція для виходу користувача
def logout_view(request):
    request.session.flush()  # очищаємо всі дані сесії (видаляємо інформацію про користувача)
    messages.success(request, 'Ви вийшли з системи.')
    return redirect('login')  # перенаправляємо на сторінку входу

# основна функція для передбачення схвалення займу
def predict(request):
    # спочатку перевіряємо чи користувач залогінився
    # якщо в сесії немає user_id, значить користувач не залогінений
    if 'user_id' not in request.session:
        messages.warning(request, 'Будь ласка, увійдіть в систему.')
        return redirect('login')
    
    # перевіряємо чи завантажена модель машинного навчання
    if model is None:
        messages.error(request, 'Модель не завантажена!')
        return render(request, 'loan_form.html', {'form': LoanForm()})
    
    # перевіряємо чи завантажений список стовпців (потрібен для правильного формату даних)
    if feature_columns is None:
        messages.error(request, 'Список стовпців не завантажено!')
        return render(request, 'loan_form.html', {'form': LoanForm()})
    
    # якщо користувач відправив форму (POST запит)
    if request.method == 'POST':
        form = LoanForm(request.POST)
        
        if form.is_valid():
            # отримуємо дані з форми
            data = form.cleaned_data.copy()  # copy() щоб не змінювати оригінальні дані
            
            # обробляємо поле Dependents - воно приходить як рядок, а треба число
            # особливий випадок: '3' означає "3 або більше", тому ставимо просто 3
            if data['Dependents'] == '3':
                data['Dependents'] = 3
            else:
                data['Dependents'] = int(data['Dependents'])  # перетворюємо рядок в число
            
            # обробляємо Credit_History - теж треба число (1 або 0)
            data['Credit_History'] = int(data['Credit_History'])
            
            # обробляємо CoapplicantIncome - якщо поле порожнє, ставимо 0
            if data.get('CoapplicantIncome') is None or data['CoapplicantIncome'] == '':
                data['CoapplicantIncome'] = 0.0
            else:
                data['CoapplicantIncome'] = float(data['CoapplicantIncome'])  # перетворюємо в десяткове число
            
            # тепер треба перетворити дані в DataFrame (таблицю pandas)
            # модель машинного навчання очікує дані в тому ж форматі, що і при навчанні
            # тому важливо зберігати правильний порядок стовпців!
            if feature_columns and model:
                # створюємо список з даними в правильному порядку
                # використовуємо feature_columns щоб знати в якому порядку мають бути стовпці
                row_data = []  # тут будуть дані для одного рядка таблиці
                for col in feature_columns:  # проходимо по кожному стовпцю в правильному порядку
                    if col in data:  # якщо стовпець є в даних з форми
                        value = data[col]
                        # обробляємо числові стовпці (доходи, сума займу тощо)
                        if col in ['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term']:
                            try:
                                row_data.append(float(value))  # перетворюємо в десяткове число
                            except (ValueError, TypeError):
                                row_data.append(0.0)  # якщо помилка, ставимо 0
                        elif col in ['Dependents', 'Credit_History']:
                            try:
                                row_data.append(int(value))  # перетворюємо в ціле число
                            except (ValueError, TypeError):
                                row_data.append(0)
                        else:
                            # категоріальні стовпці (стать, освіта тощо) - залишаємо рядками
                            row_data.append(str(value))
                    else:
                        # якщо стовпець відсутній в даних, ставимо значення за замовчуванням
                        if col in ['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term']:
                            row_data.append(0.0)
                        elif col in ['Dependents', 'Credit_History']:
                            row_data.append(0)
                        else:
                            row_data.append('')
                
                # створюємо DataFrame (таблицю) з одним рядком даних
                # columns=feature_columns вказує назви стовпців в правильному порядку
                df = pd.DataFrame([row_data], columns=feature_columns)
                
                # переконуємося що типи даних правильні (це важливо для моделі!)
                numeric_cols = ['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term']
                int_cols = ['Dependents', 'Credit_History']
                
                # конвертуємо числові стовпці в float (десяткові числа)
                for col in numeric_cols:
                    if col in df.columns:
                        # to_numeric() перетворює в число, errors='coerce' означає що помилки стають NaN
                        # fillna(0.0) замінює NaN на 0, astype(float) перетворює в тип float
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0).astype(float)
                
                # конвертуємо цілочисельні стовпці в int
                for col in int_cols:
                    if col in df.columns:
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
                
                # категоріальні стовпці (стать, освіта тощо) залишаємо як рядки (object)
                for col in df.columns:
                    if col not in numeric_cols and col not in int_cols:
                        df[col] = df[col].astype(str)
            else:
                # якщо немає feature_columns (не повинно бути, але на всяк випадок)
                df = pd.DataFrame([data])
            
            # обгортаємо в try/except щоб ловити помилки
            try:
                # перевірки перед викликом моделі
                if not isinstance(df, pd.DataFrame):
                    raise ValueError(f"df має бути DataFrame, а не {type(df)}")
                
                # перевіряємо що DataFrame має правильну форму (1 рядок, N стовпців)
                if df.shape[0] != 1:
                    raise ValueError(f"df має мати 1 рядок, але має {df.shape[0]}")
                
                # перевіряємо що DataFrame не порожній
                if df.empty:
                    raise ValueError("DataFrame порожній")
                
                # викликаємо модель для передбачення!
                # model - це Pipeline з scikit-learn, він автоматично:
                # 1. Застосує preprocessor (StandardScaler для чисел, OneHotEncoder для категорій)
                # 2. Зробить передбачення через RandomForestClassifier
                prediction = model.predict(df)[0]  # predict() повертає масив, беремо перший елемент [0]
                probability = model.predict_proba(df)[0]  # predict_proba() повертає ймовірності для кожного класу
                
                # отримуємо порядок класів з моделі (зазвичай ['N', 'Y'])
                classes = model.classes_
                
                # знаходимо індекси для 'Y' (Yes - схвалено) та 'N' (No - відхилено)
                # це потрібно щоб правильно інтерпретувати ймовірності
                y_idx = None
                n_idx = None
                for i, cls in enumerate(classes):  # enumerate дає індекс і значення
                    if cls == 'Y':
                        y_idx = i
                    elif cls == 'N':
                        n_idx = i
                
                # якщо не знайшли класи (не повинно бути, але на всяк випадок)
                if y_idx is None or n_idx is None:
                    # припускаємо стандартний порядок ['N', 'Y']
                    y_idx = 1
                    n_idx = 0
                
                # обчислюємо ймовірності у відсотках
                prob_approved = probability[y_idx] * 100  # ймовірність схвалення
                prob_rejected = probability[n_idx] * 100  # ймовірність відхилення
                
                # формуємо словник з результатами для передачі в шаблон
                result = {
                    'prediction': 'Схвалено' if prediction == 'Y' else 'Відхилено',  # текстовий результат
                    'probability_approved': round(prob_approved, 2),  # округлюємо до 2 знаків після коми
                    'probability_rejected': round(prob_rejected, 2),
                    'input_data': data  # зберігаємо вхідні дані щоб показати користувачу
                }
                
                # показуємо сторінку з результатом
                return render(request, 'result.html', {'result': result})
            except Exception as e:
                # якщо сталася помилка, ловимо її тут
                import traceback
                error_msg = f'Помилка при передбаченні: {str(e)}'
                print(f"Помилка при передбаченні: {error_msg}")
                print(traceback.format_exc())  # виводимо детальну інформацію про помилку
                messages.error(request, error_msg)  # показуємо помилку користувачу
                return render(request, 'loan_form.html', {'form': form})
        else:
            # якщо форма не валідна (користувач ввів неправильні дані)
            messages.error(request, 'Будь ласка, виправте помилки у формі.')
    else:
        # якщо це GET запит (просто відкрили сторінку), показуємо порожню форму
        form = LoanForm()
    
    # показуємо HTML сторінку з формою
    return render(request, 'loan_form.html', {'form': form})

