from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import User, Task, Category, History, Profile

from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.models import BaseUserManager

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = (
      'id',
      'email', 'first_name', 'last_name')
  #ユーザを作る際に使用するcreateメソッドをオーバーライドする。
  def create(self,validated_data):
      user = User.objects.create(**validated_data)
      #トークンを生成する
      Token.objects.create(user=user)
      return user


class UserIdSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'first_name', 'last_name')


class CategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = (
      'id',
      'category_name', 'color_code', 'user_id')
    read_only_fields = ('id','user_id',)

  def create(self, validated_data):
    category = Category(
        category_name=validated_data['category_name'],
        color_code=validated_data['color_code'],
        user_id_id=self.context['request'].user.id
    )
    category.save()
    return category


class TaskSerializer(serializers.ModelSerializer):
  category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(),many=True)
  class Meta:
    model = Task
    fields = (
      'id',
      'title', 'detail', 'url', 'created_at', 'priority','next_display_date','display_times','consecutive_times','is_update','user_id', 'category')
      # depth= 1
    read_only_fields = ('id','priority','user_id','display_times','consecutive_times','is_update',)


class HistorySerializer(serializers.ModelSerializer):
  class Meta:
    model = History
    fields = (
      'id',
      'completed_date', 'feedback', 'user_id', 'task_id')
    read_only_fields = ('id','completed_date', 'user_id',)

class TaskCompletedSerializer(serializers.ModelSerializer):
  class Meta:
    model = Task
    fields = (
      'id',
      'priority','next_display_date','display_times','consecutive_times','is_update')
    read_only_fields = ('id','priority','next_display_date','display_times','consecutive_times','is_update')

    # def update(self, instance, validated_data):
    #   # Modify validated_data with the value you need
    #   return super().update(instance, validated_data)

class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)

class AuthUserSerializer(serializers.ModelSerializer):
    auth_token = serializers.SerializerMethodField()

    class Meta:
         model = User
         fields = ('id', 'email', 'is_active', 'is_staff', 'auth_token')
         read_only_fields = ('id', 'is_active', 'is_staff')

    def get_auth_token(self, obj):
        token = Token.objects.create(user=obj)
        return token.key

class AuthUserLoginSerializer(serializers.ModelSerializer):
    auth_token = serializers.SerializerMethodField()

    class Meta:
         model = User
         fields = ('id', 'email', 'is_active', 'is_staff', 'auth_token')
         read_only_fields = ('id', 'is_active', 'is_staff')

    def get_auth_token(self, obj):
        Token.objects.get(user=obj).delete()
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
        fields = ('id', 'email', 'password')

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

class ProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = Profile
    fields = ('id', 'username', 'is_notification', 'task_limit','update_time', 'user_id')
    read_only_fields = ('id', 'user_id',)
