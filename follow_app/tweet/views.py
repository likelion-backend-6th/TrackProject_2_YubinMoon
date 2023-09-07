from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Follow, Image, Post
from .serializer import PostSerializer, PostCreateSerializer, FollowSerializer


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


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return PostCreateSerializer
        return super().get_serializer_class()

    def list(self, request, *args, **kwargs):
        user = request.user
        follow_list = Follow.objects.filter(user=user).values_list("pk", flat=True)
        posts = Post.objects.filter(owner__in=follow_list).all()
        serializer = PostSerializer(posts, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def create(self, request, *args, **kwargs):
        user = request.user
        content = request.data.get("content")
        image = request.data.get("image")
        img = None
        if image:
            url = self.upload_image(image)
            img = Image.objects.create(url=url)
        post = Post.objects.create(owner=user, content=content, image=img)
        serializer = PostSerializer(post)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

    def update(self, request, *args, pk=None, **kwargs):
        user = request.user
        post = get_object_or_404(Post, pk=pk)
        if post.owner != user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        content = request.data.get("content")
        image = request.data.get("image")
        img = None
        if image:
            url = self.upload_image(image)
            img = Image.objects.create(url=url)
        post.content = content
        post.image = img
        post.save()
        return Response(status=status.HTTP_200_OK, data=PostSerializer(post).data)

    def upload_image(self, image) -> str:
        return "just image"

    def destroy(self, request, *args, pk=None, **kwargs):
        user = request.user
        post = get_object_or_404(Post, pk=pk)
        if post.owner != user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def list(self, request, *args, **kwargs):
        follow_list = Follow.objects.filter(user=request.user).all()
        serializer = FollowSerializer(follow_list, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=False, methods=["GET"])
    def follower(self, request, *args, **kwargs):
        follow_list = Follow.objects.filter(follow=request.user).all()
        serializer = FollowSerializer(follow_list, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
