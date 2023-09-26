from rest_framework import status
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.serializers import UserRegistrationSerializer

from rest_framework_simplejwt.views import TokenObtainPairView


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    This view allows users to obtain an access token by providing their
    email and password. The access token is used for authentication and
    authorization when making requests to protected endpoints.

    HTTP POST:
    - 200 OK: Access token obtained successfully.
    - 400 Bad Request: Invalid request data.
    - 401 Unauthorized: User email is not verified. Check your email.
    """

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            email = request.data.get('email')
            user = User.objects.filter(email=email).first()

            if user is not None and not user.is_verified:
                return Response({
                    "detail": "Your email is not verified, check your email."}, status=401)

        return response


class UserRegistrationCreateAPIView(CreateAPIView):
    """
    This view allows users to register by providing their email and password.
    Upon successful registration, a verification email with a unique
    verification number is sent to the user's email address. Users must
    verify their email by clicking the provided link to activate their account.

    HTTP POST:
    - 201 Created: User successfully registered.
    - 400 Bad Request: Invalid request data.
    - 409 Conflict: Email address is already registered.
    """
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response({'message': 'Registration was successful. Check your email for verification.'},
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserEmailVerificationAPIView(APIView):
    """
    Activates a user's account when a valid 'verification_number' query parameter
    is provided in the URL.

    HTTP GET:
    - 200 OK: User account activated.
    - 400 Bad Request: Missing 'verification_number' query parameter.
    - 404 Not Found: 'verification_number' does not match any user profile.
    """
    @staticmethod
    def get(request):
        verification_number = request.GET.get('verification_number')

        if not verification_number:
            return Response(
                {"detail": "Verification number is missing."}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, verification_number=verification_number)

        user.verification_number = None
        user.is_verified = True
        user.save()

        return Response({"detail": "You were verified successfully."}, status=status.HTTP_200_OK)
