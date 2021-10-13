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

#viewの操作のため
from rest_framework import status
from rest_framework.response import Response

# 次回表示日の設定
import datetime


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

  def post(self, request, *args, **kwargs):
    a_Post = History.objects.create(
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



class CategoryViewSet(viewsets.ModelViewSet, UserQueryset):
  queryset = Category.objects.all()
  serializer_class = CategorySerializer


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