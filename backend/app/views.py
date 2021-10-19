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
from .serializer import AuthUserSerializer, TaskSerializer, CategorySerializer, HistorySerializer, TaskCompletedSerializer, SettingSerializer

#viewの操作のため
from rest_framework import status, viewsets
from rest_framework.response import Response

# 次回表示日の設定
import datetime

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
      query_set = queryset.filter(user_id=self.request.user)
      return query_set

class SettingViewSet(viewsets.ModelViewSet):
  queryset = Setting.objects.all()
  serializer_class = SettingSerializer


class TaskViewSet(viewsets.ModelViewSet, UserQueryset):
  queryset = Task.objects.all()
  serializer_class = TaskSerializer

  def perform_create(self, serializer):
    serializer.save(user_id=self.request.user)

  def get_queryset(self):
      queryset = self.queryset
      query_set = queryset.filter(user_id=self.request.user)
      return query_set

# 日ごとのタスク表示
class TaskDailyAPIView(generics.ListAPIView):
  queryset = Task.objects.all()
  serializer_class = TaskSerializer

  def get_queryset(self):
    queryset = self.queryset
    query_set = queryset.filter(user_id=self.request.user, next_display_date__year = self.kwargs.get('year'), next_display_date__month = self.kwargs.get('month'), next_display_date__day = self.kwargs.get('day'))
    return query_set

# 月ごとのごとのタスク表示
class TaskMonthlyAPIView(generics.ListAPIView):
  queryset = Task.objects.all()
  serializer_class = TaskSerializer

  def get_queryset(self):
    queryset = self.queryset
    query_set = queryset.filter(user_id=self.request.user, next_display_date__year = self.kwargs.get('year'), next_display_date__month = self.kwargs.get('month'))
    return query_set

# タスクが完了した時の処理1(historyの追加)
class TaskCompletedHistoryAPIView(generics.CreateAPIView):
  # Historyに完了したタスクを追加
  queryset = History.objects.all()
  serializer_class = HistorySerializer

  def post(self, request, *args, **kwargs):
    a_Post = History.objects.create(
      completed_date=date.today(),
      user_id_id=self.request.user.id,
      feedback=request.data["feedback"],
      task_id_id=request.data["task_id"],
    )
    return Response(
      data=HistorySerializer(a_Post).data,
      status=status.HTTP_201_CREATED
    )


# タスクが完了した時の処理2(taskの次回表示日と優先度の更新)
class TaskCompletedTaskAPIView(generics.UpdateAPIView):
  queryset = Task.objects.all()
  serializer_class = TaskCompletedSerializer

  def update(self, request, pk=None):
    instance = self.get_object()
    feedback = request.data["feedback"]

    # 表示回数を記録
    instance.display_times = instance.display_times + 1
    display_times = instance.display_times

    # 優先度を設定
    if feedback == 2:
      if display_times == 1:
        instance.priority = 30
      elif display_times == 2:
        instance.priority = 10
      elif display_times == 3:
        instance.priority = 1
    elif feedback == 1:
      if display_times == 1:
        instance.priority = 38
      elif display_times == 2:
        instance.priority = 16
      elif display_times == 3:
        instance.priority = 2
    elif feedback == 0:
      if display_times == 1:
        instance.priority = 47
      elif display_times == 2:
        instance.priority = 21
      elif display_times == 3:
        instance.priority = 3

    # 次回表示日を設定
    if display_times == 1:
      instance.next_display_date = instance.next_display_date + datetime.timedelta(days=1)
    elif display_times == 2:
      instance.next_display_date = instance.next_display_date + datetime.timedelta(weeks=1)
    elif display_times == 3:
      instance.next_display_date = instance.next_display_date + datetime.timedelta(weeks=4)

    # feedbackが連続で2の回数を記録
    if feedback == 2:
      instance.consecutive_times = instance.consecutive_times + 1
    else:
      instance.consecutive_times = 0

    # 連続でfeedbackが2，もしくは表示回数が4回あったらタスクの終了
    if instance.consecutive_times == 2 or instance.display_times == 4:
      instance.is_update = False

    serializer = self.get_serializer(instance, data=request.data)
    serializer.is_valid(raise_exception=True)
    self.perform_update(serializer)
    instance.save()

    return Response(
      serializer.data,
      status=status.HTTP_200_OK
    )


class CategoryViewSet(viewsets.ModelViewSet):
  queryset = Category.objects.all()
  serializer_class = CategorySerializer

  def get_queryset(self):
      queryset = self.queryset
      query_set = queryset.filter(user_id=self.request.user)
      return query_set


class HistoryViewSet(viewsets.ModelViewSet):
  queryset = History.objects.all()
  serializer_class = HistorySerializer

  def get_queryset(self):
      queryset = self.queryset
      query_set = queryset.filter(user_id=self.request.user)
      return query_set


# 日ごとのヒストリー表示
class HistoryDailyAPIView(generics.ListAPIView):
  queryset = History.objects.all()
  serializer_class = HistorySerializer

  def get_queryset(self):
    queryset = self.queryset
    query_set = queryset.filter(user_id=self.request.user.id, completed_date__year = self.kwargs.get('year'), completed_date__month = self.kwargs.get('month'), completed_date__day = self.kwargs.get('day'))
    return query_set

# 月ごとのごとのヒストリー表示
class HistoryMonthlyAPIView(generics.ListAPIView):
  queryset = History.objects.all()
  serializer_class = HistorySerializer

  def get_queryset(self):
    queryset = self.queryset
    query_set = queryset.filter(user_id=self.request.user.id, completed_date__year = self.kwargs.get('year'), completed_date__month = self.kwargs.get('month'))
    return query_set


class ManageUserView(generics.RetrieveUpdateAPIView, UserQueryset):
  serializer_class = AuthUserSerializer

  #認証が通ったユーザのみアクセスできるように指定する
  authentication_classes = (TokenAuthentication,)

  #ログインしているユーザのみ許可するように指定する
  permission_classes = (IsAuthenticated,)

  #ログインしているユーザ情報を返す関数
  def get_object(self):
    return self.request.user

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
        serializers = self.get_serializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        user = get_and_authenticate_user(**serializers.validated_data)
        data = serializer.AuthUserLoginSerializer(user).data
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['POST', ], detail=False)
    def register(self, request):
        serializers = self.get_serializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        user = create_user_account(**serializers.validated_data)
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
