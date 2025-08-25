from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import BookSerializer,UserSerializer,Bserializer,bookSerializer
from rest_framework.views import APIView
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100

def get_tokens_for_user(user):
    if not user.is_active:
      raise AuthenticationFailed("User is not active")

    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class userregister(APIView):
    def post(self,request):
        
        serializers=UserSerializer(data=request.data)
        if serializers.is_valid():
            emp=serializers.save()
            token=get_tokens_for_user(emp)
            return Response({'token': token, 'data':serializers.data}, status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')
        

        return Response({'token': get_tokens_for_user(user), 'data':UserSerializer(user).data}, status=status.HTTP_200_OK)
        
class ProfileView(APIView):
    def get_permissions(self):
        if self.request.method in ["GET", "POST"]:
            return []  # No permission required
        return [IsAuthenticated()]  # For PUT, DELETE
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request):
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AllUsers(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class BookList(APIView):
     pagination_class = StandardResultsSetPagination

     permission_classes = [permissions.IsAuthenticatedOrReadOnly]

     def post(self, request):
         serializer = bookSerializer(data=request.data)
         if serializer.is_valid():
             # author = User.objects.get(id=request.user.id)
             serializer.save(author=request.user)
             return Response(serializer.data, status=status.HTTP_201_CREATED)
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
     def get(self, request):
         
         if request.user.is_authenticated:
             #author = User.objects.get(id=request.user.id)
             books = BOOK.objects.filter(author=request.user)
         else:
             books = BOOK.objects.all()
         books = BOOK.objects.all()
         paginator = self.pagination_class()
         result_page = paginator.paginate_queryset(books, request)
         serializer = bookSerializer(result_page, many=True)
         response = paginator.get_paginated_response(serializer.data)
         next_link = response.data['next']
         if next_link:
             response.data['next_page'] = next_link
         return response

    
     def delete(self, request,pk):
         #author = User.objects.get(id=request.user.id)
         books = BOOK.objects.get(author=request.user,pk=pk)
         books.delete()

   
         return Response(status=status.HTTP_204_NO_CONTENT)
    
     def put (self, request,pk):
         #author = User.objects.get(id=request.user.id)
         books = BOOK.objects.get(author=request.user,pk=pk)
         serializer = BookSerializer(books, data=request.data)
         if serializer.is_valid():
             serializer.save()
             return Response(serializer.data)
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







# from rest_framework import viewsets, status
# from rest_framework.response import Response
# from django.shortcuts import get_object_or_404
# from .models import *
# from .serializers import *
# from .pagination import BookPagination





# class BookViewSet(viewsets.ViewSet):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     # GET /books/  → List all
#     def list(self, request):

#         if request.user.is_authenticated:
#             #author = User.objects.get(id=request.user.id)
#             books = BOOK.objects.filter(author=request.user)
#         else:
#             books = BOOK.objects.all()
#         serializer = Bserializer(books, many=True)
        
#         return Response(serializer.data)

#     # POST /books/  → Create new
#     def create(self, request):
#         serializer = BookSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(author=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     # GET /books/{id}/  → Retrieve single
#     # def retrieve(self, request, pk=None):
#     #     book = get_object_or_404(BOOK, pk=pk)
#     #     serializer = Bserializer(book)
#     #     return Response(serializer.data)

#     # PUT /books/{id}/  → Update
#     def update(self, request, pk):
#         books = BOOK.objects.get(author=request.user,pk=pk)
#         serializer = BookSerializer(books, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     # DELETE /books/{id}/  → Delete
#     def destroy(self, request, pk=None):
#         book = get_object_or_404(BOOK, pk=pk)
#         book.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class UserRegister(viewsets.ViewSet):
#     def create(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# def get_tokens_for_user(user):
#      if not user.is_active:
#        raise AuthenticationFailed("User is not active")

#      refresh = RefreshToken.for_user(user)

#      return {
#          'refresh': str(refresh),
#          'access': str(refresh.access_token),
#      }


# class loginview(viewsets.ViewSet):
    # def create(self, request):
    #     email = request.data.get('email')
    #     password = request.data.get('password')

    #     user = User.objects.filter(email=email).first()

    #     if user is None:
    #         raise AuthenticationFailed('User not found')

    #     if not user.check_password(password):
    #         raise AuthenticationFailed('Incorrect password')
        

    #     return Response({'token': get_tokens_for_user(user), 'data':UserSerializer(user).data}, status=status.HTTP_200_OK)