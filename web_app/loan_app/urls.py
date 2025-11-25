# головний файл налаштування URL для всього проєкту
from django.contrib import admin  # адмін-панель Django
from django.urls import path, include  # path для маршрутів, include для підключення інших url файлів

# urlpatterns - список всіх URL маршрутів проєкту
urlpatterns = [
    path('admin/', admin.site.urls),  # адмін-панель Django (доступна за /admin/)
    path('', include('predictor.urls')),  # підключаємо URL з додатку predictor
    # include() дозволяє підключити URL з іншого файлу (з predictor/urls.py)
]


