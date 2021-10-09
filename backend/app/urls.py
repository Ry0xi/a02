from rest_framework import routers
from django.urls import path, include
from .views import UserViewSet, TaskViewSet, CategoryViewSet, HistoryViewSet, ManageUserView, TaskDailyAPIView, TaskMonthlyAPIView, SettingLimitViewSet, SignupViewSet

router = routers.DefaultRouter()
router.register('user', UserViewSet)
router.register('task', TaskViewSet)
router.register('category', CategoryViewSet)
router.register('history', HistoryViewSet)

urlpatterns = [
    path('myself/',ManageUserView.as_view( ), name='myself'),
    #ユーザ名とパスワードをPOSTするとトークンを返す。
    path('',include(router.urls)),
    path('task/<int:year>/<int:month>/<int:day>/', TaskDailyAPIView.as_view(),name='daily'),
    path('task/<int:year>/<int:month>/', TaskMonthlyAPIView.as_view(),name='monthly'),
    path('setting-limit/',SettingLimitViewSet.as_view( ), name='setting-limit'),
    path('sign_up/',SignupViewSet.as_view( ), name='sign_up'),
]