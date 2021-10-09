from rest_framework import routers
from django.urls import path, include
from .views import UserViewSet, TaskViewSet, CategoryViewSet, HistoryViewSet, ManageUserView, SettingLimitViewSet

router = routers.DefaultRouter()
router.register('user', UserViewSet)
router.register('task', TaskViewSet)
router.register('category', CategoryViewSet)
router.register('history', HistoryViewSet)

urlpatterns = [
    path('myself/',ManageUserView.as_view( ), name='myself'),
    path('setting-limit/',SettingLimitViewSet.as_view( ), name='setting-limit'),
    #ユーザ名とパスワードをPOSTするとトークンを返す。
    path('',include(router.urls)),
]