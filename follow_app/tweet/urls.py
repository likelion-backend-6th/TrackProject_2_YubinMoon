from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("", views.PostViewSet, basename="post")

user_patterns = [
    path("posts/", views.UserPostsAPIView.as_view(), name="user-posts"),
    path("signup/", views.UserSignupAPIView.as_view(), name="user-signup"),
    path("login/", views.UserLoginAPIView.as_view(), name="user-login"),
    path("logout/", views.UserLogoutAPIView.as_view(), name="user-logout"),
]

urlpatterns = [
    path("users/", views.UserListAPIView.as_view(), name="user-list"),
    path("following/", views.FollowingAPIView.as_view(), name="following-list"),
    path("follower/", views.FollowerAPIView.as_view(), name="follower-list"),
    path("follow/", views.FollowAPIView.as_view(), name="follow"),
    path("user/", include(user_patterns)),
    path("post/", include(router.urls)),
]
