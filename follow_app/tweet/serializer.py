from rest_framework import serializers
from .models import Follow, Image, Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ["owner", "created_at", "updated_at"]
