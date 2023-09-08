import os
import uuid

import boto3
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Follow, Image, Post
from .serializer import (
    CreateFollowSerializer,
    FollowSerializer,
    PostCreateSerializer,
    PostSerializer,
    UserListSerializer,
    UserSerializer,
)


@extend_schema(tags=["User"])
class UserViewSet(viewsets.ViewSet):
    @extend_schema(
        summary="전체 유저 조회",
        description="본인을 제외한 모든 유저를 조회",
        responses={200: UserListSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        user = request.user
        user_list = User.objects.exclude(pk=user.pk).all()
        data = []
        for u in user_list:
            serializer = UserListSerializer(
                data={
                    "user": UserSerializer(u).data,
                    "following": Follow.objects.filter(user=u, follow=user).exists(),
                }
            )
            if not serializer.is_valid():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            data.append(serializer.data)
        return Response(status=status.HTTP_200_OK, data=data)

    @extend_schema(
        summary="유저의 전체 개시물 조회",
        description="유저가 작성한 모든 개시물을 조회",
        responses={200: PostSerializer(many=True)},
    )
    @action(detail=False, methods=["get"])
    def posts(self, request, *args, **kwargs):
        user = request.user
        posts = Post.objects.filter(owner=user)
        serializer = PostSerializer(posts, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)


@extend_schema(tags=["Post"], description="개시물과 관련된 API")
class PostViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return PostCreateSerializer
        return super().get_serializer_class()

    @extend_schema(
        summary="팔로우의 전체 개시물 조회",
        description="팔로우한 유저가 작성한 모든 개시물을 조회",
        responses={200: PostSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        user = request.user
        follow_list = Follow.objects.filter(user=user).values_list("pk", flat=True)
        posts = Post.objects.filter(owner__in=follow_list).all()
        serializer = PostSerializer(posts, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @extend_schema(
        summary="개시물 생성",
        description="새로운 개시물 작성",
        request=PostCreateSerializer,
        responses={200: PostSerializer()},
    )
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

    @extend_schema(
        summary="개시물 수정",
        description="개시물 내용 수정",
        request=PostCreateSerializer,
        responses={200: PostSerializer()},
    )
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
        # connect to boto3
        service_name = "s3"
        endpoint_url = "https://kr.object.ncloudstorage.com"
        access_key = os.getenv("NCP_ACCESS_KEY")
        secret_key = os.getenv("NCP_SECRET_KEY")
        print(access_key)
        s3 = boto3.client(
            service_name,
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )
        bucket_name = "follow-image"
        image_id = f"{str(uuid.uuid4())}.{image.name.split('.')[-1]}"
        s3.upload_fileobj(image.file, bucket_name, image_id)
        s3.put_object_acl(Bucket=bucket_name, Key=image_id, ACL="public-read")
        url = f"{endpoint_url}/{bucket_name}/{image_id}"
        return url

    @extend_schema(
        summary="개시물 삭제",
        description="유저의 개시물 삭제",
        responses={200: PostSerializer()},
    )
    def destroy(self, request, *args, pk=None, **kwargs):
        user = request.user
        post = get_object_or_404(Post, pk=pk)
        if post.owner != user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


@extend_schema(tags=["Follow"], description="팔로우와 관련된 API")
class FollowViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return CreateFollowSerializer
        return super().get_serializer_class()

    @extend_schema(
        summary="팔로우 목록",
        description="유저가 팔로우한 유저 목록",
        responses={200: FollowSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        follow_list = Follow.objects.filter(user=request.user).all()
        serializer = FollowSerializer(follow_list, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @extend_schema(
        summary="팔로워 목록",
        description="유저를 팔로우한 유저 목록",
        responses={200: FollowSerializer(many=True)},
    )
    @action(detail=False, methods=["GET"])
    def follower(self, request, *args, **kwargs):
        follow_list = Follow.objects.filter(follow=request.user).all()
        serializer = FollowSerializer(follow_list, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @extend_schema(
        summary="팔로우",
        description="새로운 유저 팔로우",
        request=CreateFollowSerializer,
        responses={200: FollowSerializer(many=True)},
    )
    def create(self, request, *args, **kwargs):
        user = request.user
        follow_pk = request.data.get("follow")
        follow = get_object_or_404(User, pk=follow_pk)
        if follow == user:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"detail": "can't follow yourself"},
            )
        exist = Follow.objects.filter(user=user, follow=follow).first()
        if exist:
            return Response(
                status=status.HTTP_302_FOUND, data=FollowSerializer(exist).data
            )
        follow = Follow.objects.create(user=user, follow=follow)
        serializer = FollowSerializer(follow)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

    @extend_schema(
        summary="언팔로우",
        description="선택한 유저 언팔로우",
        responses={200: FollowSerializer(many=True)},
    )
    def destroy(self, request, *args, pk=None, **kwargs):
        user = request.user
        follow_user = get_object_or_404(User, pk=pk)
        follow = Follow.objects.filter(user=user, follow=follow_user).first()
        if follow:
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
