from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from habits.apps import HabitsConfig
from users.views import (
    UserRegistrationCreateAPIView, CustomTokenObtainPairView, UserEmailVerificationAPIView
)

app_name = HabitsConfig.name

urlpatterns = [
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/registration/', UserRegistrationCreateAPIView.as_view(), name='registration'),
    path('api/verification/', UserEmailVerificationAPIView.as_view(), name='verification'),
]
