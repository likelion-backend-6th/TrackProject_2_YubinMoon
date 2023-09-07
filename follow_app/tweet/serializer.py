from rest_framework import serializers
from .models import Follow, Image, Post


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
