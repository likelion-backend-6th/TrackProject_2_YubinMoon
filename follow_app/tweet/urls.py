from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("post", views.PostViewSet, basename="post")

user_patterns = [
    path("posts/", views.UserPostsAPIView.as_view(), name="user-posts"),
]

urlpatterns = [
    path("users/", views.UserListAPIView.as_view(), name="user-list"),
    path("user/", include(user_patterns)),
    path("", include(router.urls)),
]
