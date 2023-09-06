from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import Follow, Image, Post


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

    def posts(self, request, *args, **kwargs):
        return Response({"message": "Hello, world!"})
