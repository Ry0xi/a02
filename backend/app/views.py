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
from .models import User, Task, Category, History, Setting
from .serializer import AuthUserSerializer, TaskSerializer, CategorySerializer, HistorySerializer, SettingSerializer

from rest_framework.response import Response
from rest_framework import status, viewsets

from django.contrib.auth import get_user_model, logout
from django.core.exceptions import ImproperlyConfigured
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

from . import serializer
from .utils import get_and_authenticate_user, create_user_account


User = get_user_model()

class UserQueryset():
  def get_queryset(self):
      queryset = self.queryset
      query_set = queryset.filter(user_id=self.request.user.id)
      return query_set

class SettingViewSet(viewsets.ModelViewSet):
  queryset = Setting.objects.all()
  serializer_class = SettingSerializer


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
  serializer_class = AuthUserSerializer

  #認証が通ったユーザのみアクセスできるように指定する
  authentication_classes = (TokenAuthentication,)

  #ログインしているユーザのみ許可するように指定する
  permission_classes = (IsAuthenticated,)

  #ログインしているユーザ情報を返す関数
  def get_object(self):
    return self.request.user


class SettingLimitViewSet(generics.UpdateAPIView):
  queryset = Setting.objects.all()
  serializer_class = SettingSerializer


# class SignupViewSet(generics.CreateAPIView):
#   queryset = User.objects.all()
#   serializer_class = AuthenticationSerializer


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]
    serializer_class = serializer.EmptySerializer
    serializer_classes = {
        'login': serializer.UserLoginSerializer,
        'register': serializer.UserRegisterSerializer,
        'password_change': serializer.PasswordChangeSerializer,
    }

    @action(methods=['POST', ], detail=False)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_and_authenticate_user(**serializer.validated_data)
        data = serializer.AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['POST', ], detail=False)
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = create_user_account(**serializer.validated_data)
        data = serializer.AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_201_CREATED)
    
    @action(methods=['POST', ], detail=False)
    def logout(self, request):
        logout(request)
        data = {'success': 'Sucessfully logged out'}
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False, permission_classes=[IsAuthenticated, ])
    def password_change(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()
