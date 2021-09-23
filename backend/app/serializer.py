from rest_framework import serializers

from .models import User, Task, Category, History

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields =('user_name', 'email_adress', 'token', 'is_notification')

class TaskSerializer(serializers.ModelSerializer):
  class Meta:
    model = Task
    fields =('title', 'detail', 'url', 'category_id')

class CategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields =('category_name', 'color_code')

class HistorySerializer(serializers.ModelSerializer):
  class Meta:
    model = History
    fields =('date', 'feedback', 'number_of_tasks', 'execution_tasks', 'task_id')