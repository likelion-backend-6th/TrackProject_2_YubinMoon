from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("user", views.UserViewSet, basename="user")
router.register("post", views.PostViewSet, basename="post")
router.register("follow", views.FollowViewSet, basename="follow")
