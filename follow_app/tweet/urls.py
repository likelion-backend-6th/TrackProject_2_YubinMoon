from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("user", views.UserViewSet, basename="user")
router.register("post", views.PostViewSet, basename="post")
router.register("follow", views.FollowViewSet, basename="follow")

user_patterns = [
    path("posts/", views.UserPostsAPIView.as_view(), name="user-posts"),
]

urlpatterns = [
    path("users/", views.UserListAPIView.as_view(), name="user-list"),
    path("user/", include(user_patterns)),
    path("", include(router.urls)),
]
