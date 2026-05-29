# authentication/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    # Usamos las vistas nativas de Django, pero les especificamos nuestro propio template HTML
    path('login/', auth_views.LoginView.as_view(template_name='authentication/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    path('redirect/', views.redirect_by_role, name='redirect_by_role'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

]