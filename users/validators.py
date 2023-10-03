from rest_framework import serializers


class PasswordMatchValidator:
    """
    Checking if the password are the same.
    """

    def __init__(self, password_field, password1_field):
        self.password_field = password_field
        self.password1_field = password1_field

    def __call__(self, data):
        password = data.get(self.password_field)
        password1 = data.get(self.password1_field)

        if password and password1 and password != password1:
            raise serializers.ValidationError({
                self.password1_field: "Passwords do not match"
            })
