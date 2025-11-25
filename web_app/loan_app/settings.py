# налаштування Django для проєкту loan_app
# тут зберігаються всі налаштування проєкту: база даних, додатки, мова тощо

from pathlib import Path  # для роботи з шляхами до файлів
import os  # для роботи з операційною системою

# шлях до папки проєкту (web_app)
# __file__ - це поточний файл (settings.py)
# .parent.parent - піднімаємося на 2 рівні вище (з loan_app до web_app)
BASE_DIR = Path(__file__).resolve().parent.parent

# секретний ключ Django (використовується для шифрування сесій, паролів тощо)
# увага: для навчального проєкту можна залишити так, але в продакшені треба змінити!
SECRET_KEY = 'django-insecure-loan-prediction-project-key-change-in-production'

# режим відлагодження (True = показувати детальні помилки, False = для продакшену)
DEBUG = True

# список дозволених доменів (порожній = всі дозволені, для локальної розробки)
ALLOWED_HOSTS = []

# список встановлених додатків Django
# Django має багато вбудованих додатків (admin, auth тощо)
# predictor - це наш власний додаток

INSTALLED_APPS = [
    'django.contrib.admin',  # адмін-панель
    'django.contrib.auth',  # система автентифікації (логін/пароль)
    'django.contrib.contenttypes',  # для типів контенту
    'django.contrib.sessions',  # для роботи з сесіями
    'django.contrib.messages',  # для показу повідомлень користувачу
    'django.contrib.staticfiles',  # для статичних файлів (CSS, JS, картинки)
    'predictor',  # наш додаток для передбачення займів
]

# MIDDLEWARE - це проміжні обробники запитів
# вони виконуються для кожного HTTP запиту (як фільтри)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # безпека
    'django.contrib.sessions.middleware.SessionMiddleware',  # робота з сесіями
    'django.middleware.common.CommonMiddleware',  # загальні функції
    'django.middleware.csrf.CsrfViewMiddleware',  # захист від CSRF атак
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # автентифікація
    'django.contrib.messages.middleware.MessageMiddleware',  # повідомлення
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # захист від clickjacking
]

# головний файл з URL маршрутами
ROOT_URLCONF = 'loan_app.urls'

# налаштування шаблонів (HTML файлів)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # використовуємо Django шаблони
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # папка з шаблонами (templates/)
        'APP_DIRS': True,  # шукати шаблони в папках додатків
        'OPTIONS': {
            'context_processors': [
                # context_processors - функції які додають змінні до всіх шаблонів
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',  # інформація про користувача
                'django.contrib.messages.context_processors.messages',  # повідомлення
            ],
        },
    },
]

# WSGI застосунок (для запуску на сервері)
WSGI_APPLICATION = 'loan_app.wsgi.application'


# налаштування бази даних
# використовуємо SQLite - просту файлову базу даних (не потрібен окремий сервер)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # движок бази даних (SQLite)
        'NAME': BASE_DIR / 'db.sqlite3',  # шлях до файлу бази даних
    }
}


# валідатори паролів (перевірка складності пароля)
# у нашому проєкті не використовуються, бо паролі не хешуються
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# мова та часовий пояс

LANGUAGE_CODE = 'uk-ua'  # мова інтерфейсу (українська)

TIME_ZONE = 'Europe/Kyiv'  # часовий пояс (Київ)

USE_I18N = True  # увімкнути інтернаціоналізацію (підтримка багатьох мов)

USE_TZ = True  # використовувати часові пояси


# налаштування статичних файлів (CSS, JavaScript, картинки)

STATIC_URL = 'static/'  # URL префікс для статичних файлів
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  # папка зі статичними файлами

# тип первинного ключа для моделей (автоматично створюється поле id)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'  # великий цілочисельний ключ


