
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



# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import BookViewSet

# router = DefaultRouter()
# router.register(r'books', BookViewSet, basename='book')

# urlpatterns = [
#     path('', include(router.urls)),
# ]
# from django.urls import path, include
# from .views import *


# urlpatterns = [
#     path('book/',BookViewSet.as_view({'get':'list','post':'create'})),
#     path('book/<int:pk>',BookViewSet.as_view({'put':'update','delete':'destroy'})),
#     path('users/',UserRegister.as_view({'post':'create'})),
#     path('login/',loginview.as_view({'post':'create'})),
 

# ]