from .models import *
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BOOK
        fields = '__all__'
        read_only_fields = ('author')

class userializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =['id','name','email','is_active']

class Bserializer(serializers.ModelSerializer):
    author=userializer(read_only=True)
    class Meta:
        model = BOOK
        fields =['id','name','price','published_date','author']

class bookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BOOK
        fields = ['id','name','price','published_date','author']
        read_only_fields = ['author']