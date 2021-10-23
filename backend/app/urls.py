from rest_framework import routers
from django.urls import path, include

from .views import TaskViewSet, CategoryViewSet, HistoryViewSet, ManageUserView, TaskDailyAPIView, TaskMonthlyAPIView, HistoryDailyAPIView, HistoryMonthlyAPIView, TaskCompletedHistoryAPIView, TaskCompletedTaskAPIView
from .views import AuthViewSet, ProfileViewSet

router = routers.DefaultRouter()
router.register('auth', AuthViewSet, basename='auth')
router.register('task', TaskViewSet)
router.register('category', CategoryViewSet)
router.register('history', HistoryViewSet)
router.register('profile', ProfileViewSet)

urlpatterns = [
    path('myself/',ManageUserView.as_view( ), name='myself'),
    #ユーザ名とパスワードをPOSTするとトークンを返す。
    path('',include(router.urls)),
    path('task/<int:year>/<int:month>/<int:day>/', TaskDailyAPIView.as_view(),name='daily'),
    path('task/<int:year>/<int:month>/', TaskMonthlyAPIView.as_view(),name='monthly'),
    path('task-completed-history/',TaskCompletedHistoryAPIView.as_view(),  name='task-completed-history'),
    path('task-completed-task/<int:pk>/', TaskCompletedTaskAPIView.as_view(), name='task-completed-task'),
    path('history/<int:year>/<int:month>/<int:day>/', HistoryDailyAPIView.as_view(),name='daily'),
    path('history/<int:year>/<int:month>/', HistoryMonthlyAPIView.as_view(),name='monthly'),
    # path('setting-limit/',SettingLimitViewSet.as_view( ), name='setting-limit'),
]