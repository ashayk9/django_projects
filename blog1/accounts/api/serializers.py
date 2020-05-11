from django.contrib.auth import authenticate, login
from django.db.models import Q
from rest_framework import serializers
from django.contrib.auth.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,
                                     required=True,
                                     style={'input_type': 'password', 'placeholder': 'Password'}
                                     )

    confirm_password = serializers.CharField(write_only=True,
                                             required=True,
                                             style={'input_type': 'password', 'placeholder': 'Confirm Password'})

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'confirm_password',
        ]
        # extra_kwargs={"password":{"write_only":True},
        #               "confirm_password":{"write_only":True}
        #               }

    def validate_email(self, email):
        existing = User.objects.filter(email=email)
        if existing.exists():
            raise serializers.ValidationError("Someone with that email "
                                              "address has already registered. Was it you?")

        return email

    def validate(self, data):
        if not data.get('password') or not data.get('confirm_password'):
            raise serializers.ValidationError("Please enter a password and "
                                              "confirm it.")

        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Those passwords don't match.")

        return data

    def create(self, validated_data):
        print(validated_data)
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user_obj = User(
            username=username, email=email
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data


class UserLoginSerializer(serializers.ModelSerializer):
    token = serializers.CharField(allow_blank=True, read_only=True)
    password = serializers.CharField(write_only=True,
                                     required=True,
                                     style={'input_type': 'password', 'placeholder': 'Password'})

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'token',
        ]

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        user = User.objects.get(username=username)

        # user_obj=None
        print(user)

        if user.exists():
            user_obj = user.first()
        else:
            raise serializers.ValidationError("usename does not exist")

        if user_obj.exists():
            if not user_obj.check_password(password):
                raise serializers.ValidationError("incorrect password")

        data["data"] = "some random token"
        return data
