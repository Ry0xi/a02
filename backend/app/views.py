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
from .serializer import UserSerializer, TaskSerializer, CategorySerializer, HistorySerializer, TaskCompletedSerializer


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

# タスクが完了した時の処理1(historyの追加)
class TaskCompletedHistoryAPIView(generics.CreateAPIView):
  # Historyに完了したタスクを追加
  queryset = History.objects.all()
  serializer_class = HistorySerializer


# タスクが完了した時の処理1(historyの追加)
class TaskCompletedTaskAPIView(generics.UpdateAPIView):
  queryset = History.objects.all()
  serializer_class = TaskCompletedSerializer


class CategoryViewSet(viewsets.ModelViewSet, UserQueryset):
  queryset = Category.objects.all()
  serializer_class = CategorySerializer
  authentication_classes = (TokenAuthentication,)
  permission_classes = (IsAuthenticated,)


class HistoryViewSet(viewsets.ModelViewSet, UserQueryset):
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