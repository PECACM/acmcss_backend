import django.apps
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers

from accounts.models import Participant


def get_dynamic_serializer(cls):
    class CustomSerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
            model = cls
            fields = "__all__"

    return CustomSerializer


def get_all_model_serializers():
    all_models = django.apps.apps.get_models()
    return [get_dynamic_serializer(model) for model in all_models]


# Register serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return user


# Profile Info Serializer
class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ('contactNumber', 'accommodation', 'college', 'address', 'yearOfStudy', 'gender', 'firstTimer')


# Login Serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")
