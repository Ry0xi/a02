from rest_framework import routers
from .views import UserViewSet, TaskViewSet, CategoryViewSet, HistoryViewSet

router = routers.DefaultRouter()
router.register('user', UserViewSet)
router.register('task', TaskViewSet)
router.register('category', CategoryViewSet)
router.register('history', HistoryViewSet)