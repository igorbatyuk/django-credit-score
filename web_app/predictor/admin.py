# налаштування адмін-панелі Django
from django.contrib import admin
from .models import User  # імпортуємо нашу модель

# @admin.register - декоратор який реєструє модель в адмін-панелі
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # list_display - які поля показувати в списку користувачів
    list_display = ('id', 'name', 'email')
    # search_fields - по яких полях можна шукати
    search_fields = ('name', 'email')




