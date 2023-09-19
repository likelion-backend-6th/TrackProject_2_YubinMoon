from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiRequest
from rest_framework import mixins, serializers, status, views, viewsets
from rest_framework.response import Response

from .models import Follow, Post
from .serializer import (
    CreatePostSerializer,
    PostSerializer,
    UserSerializer,
    CommonMessage,
    SignUpSerializer,
    LoginSerializer,
)


class CommonAPIView(views.APIView):
    def get_serializer_context(self):
        return {"request": self.request, "view": self}


class CurrentUserAPIView(CommonAPIView):
    @extend_schema(
        tags=["User"],
        summary="현재 유저 조회",
        description="현재 로그인한 유저의 정보를 조회",
        responses={200: UserSerializer()},
    )
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(status=status.HTTP_200_OK, data=serializer.data)


@extend_schema(
    tags=["User"],
    summary="회원가입",
    request=SignUpSerializer,
    responses={201: CommonMessage("Successfully signed up")},
)
class UserSignupAPIView(CommonAPIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if User.objects.filter(username=username).exists():
            return Response(
                {"message": "Username already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.create_user(username=username, password=password)
        user.save()
        return Response(
            {"message": "Successfully signed up"}, status=status.HTTP_201_CREATED
        )


@extend_schema(
    tags=["User"],
    summary="로그인",
    request=LoginSerializer,
    responses={200: CommonMessage("Successfully logged in")},
)
class UserLoginAPIView(CommonAPIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response(
                {"message": "Successfully logged in"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )


@extend_schema(
    tags=["User"],
    summary="로그아웃",
    responses={200: CommonMessage("Successfully logged out")},
)
class UserLogoutAPIView(CommonAPIView):
    def get(self, request):
        logout(request)
        return Response(
            {"message": "Successfully logged out"}, status=status.HTTP_200_OK
        )


@extend_schema(
    tags=["User"],
    summary="전체 유저 조회",
    description="본인을 제외한 모든 유저를 조회",
    responses={200: UserSerializer(many=True)},
)
class UserListAPIView(CommonAPIView):
    def get(self, request):
        user_list = User.objects.exclude(pk=request.user.pk).all()
        context = self.get_serializer_context()
        serializer = UserSerializer(user_list, context=context, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)


@extend_schema(
    tags=["User"],
    summary="유저의 전체 개시물 조회",
    description="유저가 작성한 모든 개시물을 조회",
    responses={200: PostSerializer(many=True)},
)
class UserPostsAPIView(CommonAPIView):
    def get(self, request):
        user = request.user
        posts = Post.objects.filter(owner=user).all()
        serializer = PostSerializer(posts, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)


@extend_schema(
    tags=["Follow"],
    summary="팔로우 목록",
    description="유저가 팔로우한 유저 목록",
    responses={200: UserSerializer(many=True)},
)
class FollowingAPIView(CommonAPIView):
    def get(self, request):
        user = request.user
        following_users = User.objects.prefetch_related("follower").filter(
            follower__follower=user
        )
        serializer = UserSerializer(following_users, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)


@extend_schema(
    tags=["Follow"],
    summary="팔로워 목록",
    description="유저를 팔로우한 유저 목록",
    responses={200: UserSerializer(many=True)},
)
class FollowerAPIView(CommonAPIView):
    def get(self, request):
        user = request.user
        following_users = User.objects.prefetch_related("following").filter(
            following__following=user
        )
        serializer = UserSerializer(following_users, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)


@extend_schema(
    tags=["Follow"],
    summary="팔로잉 토글",
    description="유저를 팔로우 하거나 언팔로우",
    request=inline_serializer(
        name="inline serializer", fields={"user": serializers.IntegerField()}
    ),
    responses={204: None},
)
class FollowAPIView(CommonAPIView):
    def post(self, request):
        user = request.user
        follow_user = get_object_or_404(User, pk=request.data.get("user"))
        if user == follow_user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        follow = Follow.objects.filter(follower=user, following=follow_user).first()
        if follow:
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        Follow.objects.create(follower=user, following=follow_user)
        return Response(status=status.HTTP_204_NO_CONTENT)


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
        if self.action in ["create", "update"]:
            return CreatePostSerializer
        return super().get_serializer_class()

    @extend_schema(
        summary="팔로우의 전체 개시물 조회",
        description="팔로우한 유저가 작성한 모든 개시물을 조회",
        responses={200: PostSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        user = request.user
        posts = (
            Post.objects.select_related("owner")
            .prefetch_related("owner__follower")
            .filter(owner__follower__follower=user)
            .all()
        )
        serializer = PostSerializer(posts, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @extend_schema(
        summary="개시물 생성",
        description="새로운 개시물 작성",
        request=CreatePostSerializer,
        responses={200: PostSerializer()},
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        data = PostSerializer(serializer.save()).data
        return Response(status=status.HTTP_201_CREATED, data=data)

    @extend_schema(
        summary="개시물 수정",
        description="개시물 내용 수정",
        request=CreatePostSerializer,
        responses={200: PostSerializer()},
    )
    def update(self, request, *args, pk=None, **kwargs):
        user = request.user
        post = get_object_or_404(Post, pk=pk)
        if post.owner != user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(post, data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        new_post = serializer.save()
        return Response(status=status.HTTP_200_OK, data=PostSerializer(new_post).data)

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
