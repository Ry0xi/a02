import django_filters
from rest_framework import viewsets, filters

from .models import User, Task, Category, History
from .serializer import UserSerializer, TaskSerializer, CategorySerializer, HistorySerializer


class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer


class TaskViewSet(viewsets.ModelViewSet):
  queryset = Task.objects.all()
  serializer_class = TaskSerializer


class CategoryViewSet(viewsets.ModelViewSet):
  queryset = Category.objects.all()
  serializer_class = CategorySerializer


class HistoryViewSet(viewsets.ModelViewSet):
  queryset = History.objects.all()
  serializer_class = HistorySerializer
