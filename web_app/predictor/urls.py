from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('predict/', views.predict, name='predict'),
    path('logout/', views.logout_view, name='logout'),
]




