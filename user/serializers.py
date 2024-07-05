from django.contrib.auth import get_user_model
from rest_framework import serializers
from matching.models import Match
from user.models.interest import Interest
from user.models.skills import Skill
from user.models.user import Profile


CustomUser = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'confirm_password', 'bio', 'birth_date']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = CustomUser.objects.create_user(**validated_data)
        Profile.objects.create(user=user)
        return user


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'description', 'syllabus']


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'bio', 'birth_date', 'profile_picture', 'date_joined']


class ProfileSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    interests = InterestSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'skills', 'interests', 'country']


class MatchSerializer(serializers.ModelSerializer):
    user1 = UserSerializer(read_only=True)
    user2 = UserSerializer(read_only=True)

    class Meta:
        model = Match
        fields = ['id', 'user1', 'user2', 'is_accepted_by_user1', 'is_accepted_by_user2']


class MatchCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ['user1', 'user2']


class UserProfileDetailSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'bio', 'birth_date', 'profile']
        read_only_fields = ['id', 'username']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        skills_data = profile_data.pop('skills', [])
        interests_data = profile_data.pop('interests', [])

        # Update User fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update Profile fields
        profile = instance.profile
        for attr, value in profile_data.items():
            setattr(profile, attr, value)

        # Update skills and interests
        profile.skills.set([Skill.objects.get_or_create(name=skill['name'])[0] for skill in skills_data])
        profile.interests.set([Interest.objects.get_or_create(name=interest['name'])[0] for interest in interests_data])

        profile.save()

        return instance
