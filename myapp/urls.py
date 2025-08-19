
from django.urls import path
from .views import *

urlpatterns = [
    path('book/',BookList.as_view()),
    path('book/<int:pk>',BookList.as_view()),
    path('user/',userregister.as_view()),
    path('login/',LoginView.as_view()),
    path('profile/',ProfileView.as_view()),
    path('all/',AllUsers.as_view()),
    
]
