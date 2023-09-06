from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Follow, Image, Post
from .serializer import PostSerializer


class UserViewSet(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        user = request.user
        user_list = User.objects.exclude(pk=user.pk).all()
        data = []
        for u in user_list:
            data.append(
                {
                    "name": u.username,
                    "following": Follow.objects.filter(user=u, follow=user).exists(),
                }
            )
        return Response(status=status.HTTP_200_OK, data=data)

    @action(detail=False, methods=["get"])
    def posts(self, request, *args, **kwargs):
        user = request.user
        posts = Post.objects.filter(owner=user)
        serializer = PostSerializer(posts, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
