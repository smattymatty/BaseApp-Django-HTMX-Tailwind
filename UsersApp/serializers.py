from rest_framework import serializers
from .models import User, Profile


class UserProfileSerializer(serializers.ModelSerializer):
    profile_str = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'email',
                  'date_joined',
                  'profile_str',
                  'is_staff',
                  'is_active')

    def get_profile_str(self, obj):
        # Calls the __str__ method of the Profile model
        return str(obj.profile)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'  # You can specify fields you want to include
