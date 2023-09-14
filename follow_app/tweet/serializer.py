from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Follow, Image, Post


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["pk", "username"]
        read_only_fields = ["pk"]


class UserListSerializer(serializers.Serializer):
    user = UserSerializer(instance=User)
    following = serializers.BooleanField()


class PostSerializer(serializers.ModelSerializer):
    image = serializers.URLField(read_only=True)
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at"]


class PostCreateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ("owner", "created_at", "image", "updated_at")


class FollowSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    follow = UserSerializer()

    class Meta:
        model = Follow
        fields = "__all__"
        read_only_fields = ["created_at"]


class CreateFollowSerializer(serializers.ModelSerializer):
    follow = serializers.CharField(required=True)

    class Meta:
        model = Follow
        fields = "__all__"
        read_only_fields = ["user", "created_at"]


class FollowerSerializer(serializers.ModelSerializer):
    follower = UserSerializer()

    class Meta:
        model = Follow
        fields = ["follower", "created_at"]
        read_only_fields = ["created_at"]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["follower"] = UserSerializer(instance.follower).data
        return response


class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ["following", "created_at"]
        read_only_fields = ["created_at"]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["following"] = UserSerializer(instance.following).data
        return response
