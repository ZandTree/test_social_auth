from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from rest_framework import viewsets
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class BookViewset(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticated]


def github_auth(request):
    return render(request,'auth/auth.html')

