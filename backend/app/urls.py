from rest_framework import routers
from django.urls import path, include
from .views import UserViewSet, TaskViewSet, CategoryViewSet, HistoryViewSet, ManageUserView

router = routers.DefaultRouter()
router.register('user', UserViewSet)
router.register('task', TaskViewSet)
router.register('category', CategoryViewSet)
router.register('history', HistoryViewSet)
router.register('setting-limit', etting)

urlpatterns = [
    path('myself/',ManageUserView.as_view( ), name='myself'),
    #ユーザ名とパスワードをPOSTするとトークンを返す。
    path('',include(router.urls)),
]