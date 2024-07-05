from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserViewSet, ProfileViewSet, MatchViewSet, InterestViewSet, SkillViewSet, RegistrationViewSet, \
    UserProfileDetailView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'matches', MatchViewSet)
router.register(r'interests', InterestViewSet)
router.register(r'skills', SkillViewSet)
router.register(r'register', RegistrationViewSet, basename='register')


urlpatterns = [
    path('', include(router.urls)),
    path('user/profile/', UserProfileDetailView.as_view(), name='user-profile-detail'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]