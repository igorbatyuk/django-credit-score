# імпортуємо models з Django - це для створення моделей бази даних
from django.db import models

# модель користувача для бази даних
# Model - це клас Django який автоматично створює таблицю в базі даних
# спрощена версія для навчального проєкту (в реальному проєкті треба більше полів)
class User(models.Model):
    # CharField - поле для тексту обмеженої довжини
    username = models.CharField(max_length=50, unique=True)  # unique=True означає що імена мають бути унікальними
    
    # пароль - увага: не хешується! Це тільки для навчального проєкту
    # в реальному проєкті треба використовувати make_password() та check_password()
    password = models.CharField(max_length=100)
    
    # EmailField - поле для email адреси
    email = models.EmailField(blank=True)  # blank=True означає що поле необов'язкове
    
    # DateTimeField - поле для дати та часу
    created_at = models.DateTimeField(auto_now_add=True)  # auto_now_add=True автоматично ставить поточну дату при створенні
    
    # метод __str__ визначає як об'єкт буде відображатися в адмін-панелі та в консолі
    def __str__(self):
        return self.username  # повертаємо ім'я користувача
    
    # клас Meta містить метадані про модель
    class Meta:
        db_table = 'users'  # назва таблиці в базі даних (за замовчуванням Django використовує app_model)

