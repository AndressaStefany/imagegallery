from django.urls import path

from . import views
from .views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('accounts/login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('authorize/', views.authorize, name='authorize'),
    path('files/uploads/<slug:img>.<slug:ext>',views.retrieve_file, ''),
    path('help/', views.help, name='help'),
]
