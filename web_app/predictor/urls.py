# імпортуємо path для створення URL маршрутів
from django.urls import path
from . import views  # імпортуємо наші view функції

# urlpatterns - список URL маршрутів
# path(URL_шлях, функція_яку_викликати, name='назва_для_посилань')
urlpatterns = [
    path('', views.login_view, name='login'),  # головна сторінка - форма входу
    path('register/', views.register, name='register'),  # сторінка реєстрації
    path('predict/', views.predict, name='predict'),  # сторінка з формою займу та результатом
    path('logout/', views.logout_view, name='logout'),  # вихід з системи
]




