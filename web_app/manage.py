#!/usr/bin/env python
# manage.py - головний файл для управління Django проєктом
# через нього запускаються команди типу: python manage.py runserver, python manage.py migrate тощо

"""Django's command-line utility for administrative tasks."""
import os  # для роботи з операційною системою
import sys  # для роботи з системними параметрами


def main():
    """Run administrative tasks."""
    # встановлюємо змінну оточення яка вказує де знаходяться налаштування Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'loan_app.settings')
    try:
        # імпортуємо функцію для виконання команд Django
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # якщо Django не встановлено, показуємо помилку
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # виконуємо команду Django (наприклад runserver, migrate тощо)
    execute_from_command_line(sys.argv)  # sys.argv - аргументи з командного рядка


if __name__ == '__main__':
    main()  # запускаємо функцію main() коли файл виконується напряму

