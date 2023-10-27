from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from habits.paginators import HabitPaginator
from habits.permissions import IsOwnerCRUD
from habits.serializers import HabitSerializer


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator
    permission_classes = [IsAuthenticated, IsOwnerCRUD]

    def get_queryset(self):
        if self.action == 'list':
            self.queryset = Habit.objects.filter(creator=self.request.user)
        else:
            self.queryset = Habit.objects.all()
        return self.queryset


class HabitPublicAPIView(generics.ListAPIView):
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        self.queryset = Habit.objects.filter(is_public=True)
        return self.queryset