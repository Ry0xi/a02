from django.db import models
import datetime

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator

# Create your models here.

# class UserManager(BaseUserManager):
#     def _create_user(self, username, email, password=None, **extra_fields): 
#         if not username: 
#             raise ValueError('username is requied')
#         elif not email:
#             raise ValueError('Users must have an email address')

#         user = self.model(username=username, email = self.normalize_email(email), **extra_fields) # ユーザーネーム
#         user.set_password(password) # パスワード、デフォルトでハッシュになる
#         user.save(using=self._db) # トランザクションを終了する
#         return user

#     # ユーザー作成のためのやつ、adminではないユーザーを保存する _create_user を呼び出して定義
#     def create_user(self, username, email, password=None, **extra_fields):
#         extra_fields.setdefault('task_count', 0)
#         extra_fields.setdefault('is_notification', False)
#         extra_fields.setdefault('task_limit', 15)
#         extra_fields.setdefault('is_superuser', False)
#         return self._create_user(username, email, password, **extra_fields)

#     # ユーザー作成のためのやつ、adminユーザーを保存する _create_user を呼び出して定義
#     def create_superuser(self, username, email, password=None, **extra_fields):
#         extra_fields.setdefault('task_count', 0)
#         extra_fields.setdefault('is_notification', False)
#         extra_fields.setdefault('task_limit', 15)
#         extra_fields.setdefault('is_superuser', True)

#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')
#         return self._create_user(username, email, password, **extra_fields)

class User(models.Model):
    # user_id = models.AutoField(primary_key=True) #id
    user_name = models.CharField(max_length=30, null=False) #name
    email_address = models.EmailField(null=False) #mail adress
    password = models.CharField(max_length=100,null=False) #token
    task_count = models.IntegerField(default=0, null=False) #today's task count
    is_notification = models.BooleanField(default=True, null=False) #notification flag (on/off)
    task_limit = models.IntegerField(default=15, null=False) #task display limit

# class User(AbstractBaseUser, PermissionsMixin):
#     # 不正な文字列が含まれていないかチェックする
#     username_validator = UnicodeUsernameValidator()

#     user_name = models.CharField(max_length=30, unique=True, validators=[username_validator])
#     email_address = models.EmailField(null=False) #mail adress
#     task_count = models.IntegerField(default=0, null=False) #today's task count
#     is_notification = models.BooleanField(default=True, null=False) #notification flag (on/off)
#     task_limit = models.IntegerField(default=15, null=False) #task display limit
#     created_at = models.DateTimeField(default=datetime.datetime.now)

#     # ここで先ほど定義したクラスを呼び出してデフォルトのユーザーモデルとして定義する
#     objects = UserManager()

#     # ユーザーネームと必須のフィールドを定義する、ここは重複禁止
#     # 重複する場合は REQUIRED_FIELDS はからの配列を渡せば良い
#     EMAIL_FIELD = 'email_address'
#     USERNAME_FIELD = 'user_name'
#     REQUIRED_FIELDS = []


class Category(models.Model):
    # category_id = models.AutoField(primary_key=True) #id
    category_name = models.CharField(max_length=30, null=False) #name
    color_code = models.CharField(max_length=7, null=False) #color code (ex. #FF0060)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False) #user id (fk)


class Task(models.Model):
    # task_id = models.AutoField(primary_key=True) #id
    title = models.CharField(max_length=30, null=False) #task title
    detail = models.CharField(max_length=1000, null=True) #task detail
    url = models.CharField(max_length=300, null=True) #task URL
    created_at = models.DateTimeField(auto_now=True) #create datetime
    priority = models.IntegerField(default=10, null=False) #priority
    next_display_date = models.DateField(null=False) #next display date
    display_times = models.IntegerField(default=1, null=False) #Number of times displayed
    consecutive_times = models.IntegerField(default=0, null=False) #Number of consecutive achievements
    is_update = models.BooleanField(default=True, null=False) #update flag (on/off)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False) #user id (fk)
    category_id = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True) #category id (fk)


class History(models.Model):
    # history_id = models.AutoField(primary_key=True) #id
    date = models.DateField(null=False) #completed date
    feedback = models.IntegerField(default=1, null=False) #feedback number
    number_of_tasks = models.IntegerField(default=0, null=False) #today's task count
    execution_tasks = models.IntegerField(default=0, null=False) #today's execution task count
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False) #user id (fk)
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE, null=False) #task id (fk)
