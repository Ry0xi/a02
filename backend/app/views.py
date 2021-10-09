#filter用のimport
import django_filters
from datetime import date

#トークン認証に必要なライブラリ
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

#ビュー作成に必要なライブラリ
from rest_framework import generics
from rest_framework import viewsets, filters

#作成したモデルとシリアライザをインポート
from .models import User, Task, Category, History
from .serializer import UserSerializer, TaskSerializer, CategorySerializer, HistorySerializer, AuthenticationSerializer

from rest_framework.response import Response
from rest_framework import status

class UserQueryset():
  def get_queryset(self):
      queryset = self.queryset
      query_set = queryset.filter(user_id=self.request.user.id)
      return query_set

class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer


class TaskViewSet(viewsets.ModelViewSet, UserQueryset):
  queryset = Task.objects.all()
  serializer_class = TaskSerializer

# 日ごとのタスク表示
class TaskDailyAPIView(generics.ListAPIView):
  queryset = Task.objects.all()
  serializer_class = TaskSerializer

  def get_queryset(self):
    queryset = self.queryset
    query_set = queryset.filter(user_id=self.request.user.id, next_display_date__year = self.kwargs.get('year'), next_display_date__month = self.kwargs.get('month'), next_display_date__day = self.kwargs.get('day'))
    return query_set

# 月ごとのごとのタスク表示
class TaskMonthlyAPIView(generics.ListAPIView):
  queryset = Task.objects.all()
  serializer_class = TaskSerializer

  def get_queryset(self):
    queryset = self.queryset
    query_set = queryset.filter(user_id=self.request.user.id, next_display_date__year = self.kwargs.get('year'), next_display_date__month = self.kwargs.get('month'))
    return query_set


class CategoryViewSet(viewsets.ModelViewSet):
  queryset = Category.objects.all()
  serializer_class = CategorySerializer
  authentication_classes = (TokenAuthentication,)
  permission_classes = (IsAuthenticated,)


class HistoryViewSet(viewsets.ModelViewSet):
  queryset = History.objects.all()
  serializer_class = HistorySerializer


class ManageUserView(generics.RetrieveUpdateAPIView, UserQueryset):
  serializer_class = UserSerializer

  #認証が通ったユーザのみアクセスできるように指定する
  authentication_classes = (TokenAuthentication,)

  #ログインしているユーザのみ許可するように指定する
  permission_classes = (IsAuthenticated,)

  #ログインしているユーザ情報を返す関数
  def get_object(self):
    return self.request.user


class SettingLimitViewSet(generics.UpdateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer
<<<<<<< HEAD
=======
  authentication_classes = (TokenAuthentication,)
  permission_classes = (IsAuthenticated,)
>>>>>>> 899b45b3c1bffe4d77a6ddd3c40d9d1280a2069a


class SignupViewSet(generics.CreateAPIView):
  queryset = User.objects.all()
<<<<<<< HEAD
  serializer_class = AuthenticationSerializer
=======
  serializer_class = AuthenticationSerializer


# class SigninViewSet(generics.RetrieveAPIView):
#   def get_queryset(self):
#       user = self.request.user.id
#       return User.objects.filter(user_id=user)
#   serializer_class = AuthenticationSerializer
#   queryset = get_queryset
#   print(queryset)
#   queryset.auth_token.create()
#   Response(status=status.HTTP_200_OK)

>>>>>>> 899b45b3c1bffe4d77a6ddd3c40d9d1280a2069a
