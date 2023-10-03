from rest_framework import serializers, status
from rest_framework.response import Response

from users.models import User
from users.tasks import email_user_verify, generate_verification_number
from users.validators import PasswordMatchValidator


class UserRegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password1')
        validators = (PasswordMatchValidator(password_field='password', password1_field='password1'),)

    def create(self, validated_data):
        _ = validated_data.pop('password1')
        password = validated_data.pop('password')

        email = validated_data.get('email')
        verification_number = generate_verification_number()

        email_user_verify.delay(email, verification_number)

        user = User.objects.create(**validated_data, verification_number=verification_number)
        user.set_password(password)
        user.verification_number = verification_number
        user.save()

        return Response(
            {'message': 'Registration was successful. Check your email for verification.'},
            status=status.HTTP_201_CREATED
        )
