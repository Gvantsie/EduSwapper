from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status, generics, permissions
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from matching.models import Match
from .models.interest import Interest
from .models.skills import Skill
from .models.user import User, Profile
from .serializers import UserSerializer, ProfileSerializer, MatchSerializer, InterestSerializer, SkillSerializer, \
    MatchCreateSerializer, UserRegistrationSerializer, UserProfileDetailSerializer


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_description="List all users",
        responses={200: UserSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new user",
        request_body=UserSerializer,
        responses={201: UserSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class InterestViewSet(viewsets.ModelViewSet):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer


class RegistrationViewSet(viewsets.GenericViewSet):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['POST'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "user": UserSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "message": "User created successfully.",
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

    @action(detail=False, methods=['GET'])
    def potential_matches(self, request):
        user = request.user
        user_profile = user.profile
        potential_matches = Profile.objects.filter(
            skills__in=user_profile.interests.all()
        ).exclude(user=user).distinct()

        serializer = ProfileSerializer(potential_matches, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def accept_match(self, request, pk=None):
        match = self.get_object()
        user = request.user

        if match.user1 == user:
            match.is_accepted_by_user1 = True
        elif match.user2 == user:
            match.is_accepted_by_user2 = True
        else:
            return Response({"detail": "User is not part of this match"}, status=status.HTTP_400_BAD_REQUEST)

        match.save()
        return Response(MatchSerializer(match).data)

    def create(self, request, **kwargs):
        serializer = MatchCreateSerializer(data=request.data)
        if serializer.is_valid():
            match = serializer.save()
            return Response(MatchSerializer(match).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
