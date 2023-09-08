import io
import json
import tempfile
from unittest.mock import MagicMock, patch

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Follow, Image, Post
from .serializer import FollowSerializer, PostSerializer


# Create your tests here.
class UserTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.basic_user = User.objects.create(username="basic", password="basic")
        for i in range(5):
            user = User.objects.create(
                username=f"un_follow_{i}", password=f"un_follow_{i}"
            )
        for i in range(5):
            user = User.objects.create(username=f"follow_{i}", password=f"follow_{i}")
            Follow.objects.create(user=cls.basic_user, follow=user)

        for i in range(5):
            Post.objects.create(owner=cls.basic_user, content=f"content_{i}")

    def test_get_all_user(self):
        self.client.force_login(self.basic_user)
        res = self.client.get(reverse("user-list"))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = json.loads(res.content)
        all_users = User.objects.all()
        self.assertEqual(len(data), len(all_users) - 1)

    def test_get_all_post_created_by_user(self):
        self.client.force_login(self.basic_user)
        res = self.client.get(reverse("user-posts"))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = json.loads(res.content)
        user_posts = Post.objects.filter(owner=self.basic_user)
        self.assertEqual(len(data), len(user_posts))


class PostTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.basic_user = User.objects.create(username="basic", password="basic")
        for i in range(5):
            user = User.objects.create(
                username=f"un_follow_{i}", password=f"un_follow_{i}"
            )
            Post.objects.create(owner=user, content=f"content_{i}")
        for i in range(5):
            user = User.objects.create(username=f"follow_{i}", password=f"follow_{i}")
            Follow.objects.create(user=cls.basic_user, follow=user)
            Post.objects.create(owner=user, content=f"content_{i}")

        for i in range(5):
            Post.objects.create(owner=cls.basic_user, content=f"content_{i}")

    def test_get_all_follower_post(self):
        self.client.force_login(self.basic_user)
        res = self.client.get(reverse("post-list"))
        data = json.loads(res.content)
        follow_list = Follow.objects.filter(user=self.basic_user).values_list(
            "pk", flat=True
        )
        user_posts = Post.objects.filter(owner__in=follow_list).all()
        serializer = PostSerializer(user_posts, many=True)
        self.assertEqual(serializer.data, data)

    def test_write_post(self):
        self.client.force_login(self.basic_user)
        res = self.client.post(reverse("post-list"), {"content": "test content"})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        data = json.loads(res.content)
        self.assertEqual(data["content"], "test content")
        self.assertEqual(data["owner"], self.basic_user.username)

    @patch("tweet.views.PostViewSet.upload_image")
    def test_write_post_with_image(self, upload_image_mock: MagicMock):
        img_url = "https://test.com/test.jpg"
        upload_image_mock.return_value = img_url
        with tempfile.NamedTemporaryFile(suffix=".jpg") as tmpfile:
            data = {"content": "image content", "image": tmpfile}
            self.client.force_login(self.basic_user)
            res = self.client.post(reverse("post-list"), data)
            self.assertEqual(res.status_code, status.HTTP_201_CREATED)
            data = json.loads(res.content)
            self.assertEqual(data["content"], "image content")
            self.assertEqual(data["owner"], self.basic_user.username)
            self.assertEqual(data["image"], img_url)

    def test_update_post_with_permision(self):
        # post owner can update post
        self.client.force_login(self.basic_user)
        post = Post.objects.create(owner=self.basic_user, content="test content")
        res = self.client.put(
            reverse("post-detail", args=[post.pk]), {"content": "update content"}
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = json.loads(res.content)
        self.assertEqual(data["content"], "update content")
        self.assertEqual(data["owner"], self.basic_user.username)

        # other user can't update post
        other_user = User.objects.create(username="other", password="other")
        self.client.force_login(other_user)
        post = Post.objects.create(owner=self.basic_user, content="test content")
        res = self.client.put(
            reverse("post-detail", args=[post.pk]), {"content": "update content"}
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_post_with_permission(self):
        # post owner can delete post
        self.client.force_login(self.basic_user)
        post = Post.objects.create(owner=self.basic_user, content="test content")
        res = self.client.delete(reverse("post-detail", args=[post.pk]))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        # other user can't delete post
        other_user = User.objects.create(username="other", password="other")
        self.client.force_login(other_user)
        post = Post.objects.create(owner=self.basic_user, content="test content")
        res = self.client.delete(reverse("post-detail", args=[post.pk]))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class FollowTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.base_user = User.objects.create(username="base", password="base")
        for i in range(3):
            user1 = User.objects.create(
                username=f"1_follow_{i}", password=f"1_follow_{i}"
            )
            user2 = User.objects.create(
                username=f"2_follow_{i}", password=f"2_follow_{i}"
            )
            user3 = User.objects.create(
                username=f"3_follow_{i}", password=f"3_follow_{i}"
            )
            Follow.objects.create(user=cls.base_user, follow=user1)
            Follow.objects.create(user=user2, follow=cls.base_user)
            Follow.objects.create(user=cls.base_user, follow=user3)
            Follow.objects.create(user=user3, follow=cls.base_user)

    def test_get_all_following(self):
        self.client.force_login(self.base_user)
        res = self.client.get(reverse("follow-list"))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = json.loads(res.content)
        follow_list = Follow.objects.filter(user=self.base_user).all()
        serializer = FollowSerializer(follow_list, many=True)
        self.assertEqual(data, serializer.data)

    def test_get_all_followers(self):
        self.client.force_login(self.base_user)
        res = self.client.get(reverse("follow-follower"))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = json.loads(res.content)
        follower_list = Follow.objects.filter(follow=self.base_user).all()
        serializer = FollowSerializer(follower_list, many=True)
        self.assertEqual(data, serializer.data)

    def test_follow(self):
        # 정상 요청
        self.client.force_login(self.base_user)
        test_user = Follow.objects.exclude(user=self.base_user).first().user
        res = self.client.post(reverse("follow-list"), {"follow": test_user.pk})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        data = json.loads(res.content)
        self.assertEqual(data["user"]["pk"], self.base_user.pk)
        self.assertEqual(data["follow"]["pk"], test_user.pk)

        # 이미 팔로우
        self.client.force_login(self.base_user)
        follow = Follow.objects.filter(user=self.base_user).first().follow
        res = self.client.post(reverse("follow-list"), {"follow": follow.pk})
        self.assertEqual(res.status_code, status.HTTP_302_FOUND)

        # 본인과 팔로우
        self.client.force_login(self.base_user)
        res = self.client.post(reverse("follow-list"), {"follow": self.base_user.pk})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unfollow(self):
        # 존재하는 팔로우 삭제
        self.client.force_login(self.base_user)
        follow = Follow.objects.filter(user=self.base_user).first().follow
        res = self.client.delete(reverse("follow-detail", args=[follow.pk]))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        # 존재하지 않는 팔로우 삭제
        self.client.force_login(self.base_user)
        follow = Follow.objects.exclude(user=self.base_user).first().follow
        res = self.client.delete(reverse("follow-detail", args=[follow.pk]))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
