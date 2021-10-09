from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import User, Task, Category, History

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = (
      #'user_id',
      'user_name', 'email_address', 'password', 'task_count', 'is_notification')
  #ユーザを作る際に使用するcreateメソッドをオーバーライドする。
  def create(self,validated_data):
      user = User.objects.create(**validated_data)
      #トークンを生成する
      Token.objects.create(user=user)
      return user

class TaskSerializer(serializers.ModelSerializer):
  class Meta:
    model = Task
    fields = (
      #'task_id',
      'title', 'detail', 'url', 'created_at', 'priority','next_display_date','display_times','consecutive_times','is_update','user_id', 'category_id')

class CategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = (
      #'category_id',
      'category_name', 'color_code', 'user_id')

class HistorySerializer(serializers.ModelSerializer):
  class Meta:
    model = History
    fields = (
      #'history_id',
      'date', 'feedback', 'number_of_tasks', 'execution_tasks', 'user_id', 'task_id')

class AuthenticationSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('user_name', 'email_address', 'password')