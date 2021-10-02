import django_filters

#トークン認証に必要なライブラリ
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

#ビュー作成に必要なライブラリ
from rest_framework import generics
from rest_framework import viewsets, filters

#作成したモデルとシリアライザをインポート
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
  authentication_classes = (TokenAuthentication,)
  permission_classes = (IsAuthenticated,)


class HistoryViewSet(viewsets.ModelViewSet):
  queryset = History.objects.all()
  serializer_class = HistorySerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
  serializer_class = UserSerializer

  #認証が通ったユーザのみアクセスできるように指定する
  authentication_classes = (TokenAuthentication,)

  #ログインしているユーザのみ許可するように指定する
  permission_classes = (IsAuthenticated,)

  #ログインしているユーザ情報を返す関数
  def get_object(self):
    return self.request.user