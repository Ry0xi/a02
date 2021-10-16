from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import User, Task, Category, History

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
  user_id = UserIdSerializer(read_only=True)
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
      'task_id',
      'priority','next_display_date','display_times','consecutive_times','is_update')
    read_only_fields = ('task_id','priority','next_display_date','display_times','consecutive_times','is_update')

    # def update(self, instance, validated_data):
    #   # Modify validated_data with the value you need
    #   return super().update(instance, validated_data)