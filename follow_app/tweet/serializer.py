from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Follow, Image, Post
from common import image


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["pk", "username"]

    def to_representation(self, instance):
        request = self.context.get("request")
        if request is None:
            return super().to_representation(instance)
        user = request.user
        response = super().to_representation(instance)
        response["following"] = Follow.objects.filter(
            follower=user, following=instance
        ).exists()
        return response


class PostSerializer(serializers.ModelSerializer):
    image = serializers.URLField(read_only=True)

    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ["pk", "owner", "created_at", "updated_at"]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["owner"] = UserSerializer(instance.owner, context=self.context).data
        return response


class CreatePostSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = Post
        fields = ["content", "image", "private"]

    def save(self, **kwargs):
        img = self.validated_data.get("image")
        request = self.context.get("request")
        kwargs["owner"] = request.user
        if img:
            url = image.upload(img)
            img_url = Image.objects.create(url=url)
            kwargs["image"] = img_url
        return super().save(**kwargs)


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


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(label="유저명", help_text="유저명을 입력해주세요.")
    password = serializers.CharField(label="비밀번호", help_text="비밀번호를 입력해주세요.")


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(label="유저명", help_text="유저명을 입력해주세요.")
    password = serializers.CharField(label="비밀번호", help_text="비밀번호를 입력해주세요.")


class CommonMessage(serializers.Serializer):
    message = serializers.CharField(label="메시지", help_text="응답에 대한 메시지가 포함됩니다.")
