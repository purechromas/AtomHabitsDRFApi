from django.urls import path
from rest_framework.routers import DefaultRouter

from habits.apps import HabitsConfig
from habits.views import HabitViewSet, HabitPublicAPIView

app_name = HabitsConfig.name

router = DefaultRouter()
router.register(r'api/habit', viewset=HabitViewSet, basename='habit')

urlpatterns = [
    path('api/habit/public/', HabitPublicAPIView.as_view(), name='habit_public')
] + router.urls
