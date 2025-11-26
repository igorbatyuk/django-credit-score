# імпортуємо models з Django - це для створення моделей бази даних
from django.db import models

# модель користувача для бази даних
# Model - це клас Django який автоматично створює таблицю в базі даних
# спрощена версія для навчального проєкту (в реальному проєкті треба більше полів)
class User(models.Model):
    # id - автоматично створюється Django (primary key)
    
    # CharField - поле для імені користувача
    name = models.CharField(max_length=100)
    
    # EmailField - поле для email адреси (унікальне, обов'язкове)
    email = models.EmailField(unique=True)
    
    # пароль - увага: не хешується! Це тільки для навчального проєкту
    # в реальному проєкті треба використовувати make_password() та check_password()
    password = models.CharField(max_length=100)
    
    # метод __str__ визначає як об'єкт буде відображатися в адмін-панелі та в консолі
    def __str__(self):
        return self.name  # повертаємо ім'я користувача
    
    # клас Meta містить метадані про модель
    class Meta:
        db_table = 'users'  # назва таблиці в базі даних (за замовчуванням Django використовує app_model)

