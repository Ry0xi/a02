from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import User, Task, Category, History, Setting

from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.models import BaseUserManager


User = get_user_model()

class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)

class AuthUserSerializer(serializers.ModelSerializer):
    auth_token = serializers.SerializerMethodField()

    class Meta:
         model = User
         fields = ('id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')
         read_only_fields = ('id', 'is_active', 'is_staff')
    
    def get_auth_token(self, obj):
        token = Token.objects.create(user=obj)
        return token.key

class EmptySerializer(serializers.Serializer):
    pass


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    A user serializer for registering the user
    """

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name')

    def validate_email(self, value):
        user = User.objects.filter(email=value)
        if user:
            raise serializers.ValidationError("Email is already taken")
        return BaseUserManager.normalize_email(value)

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError('Current password does not match')
        return value

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value


class SettingSerializer(serializers.ModelSerializer):
  class Meta:
    model = Setting
    fields = ('username', 'is_notification', 'task_limit', 'user_id')

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
