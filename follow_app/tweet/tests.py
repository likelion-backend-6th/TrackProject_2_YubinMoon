import io
import json
import tempfile
from unittest.mock import MagicMock, patch
from PIL import Image as PImage
from io import BytesIO
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase

from .models import Follow, Image, Post
from .serializer import FollowSerializer, PostSerializer


class UserTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.basic_user = User.objects.create_user(username="basic", password="basic")
        cls.basic_user_posts = []
        for i in range(5):
            post = Post.objects.create(owner=cls.basic_user, content=f"content_{i}")
            cls.basic_user_posts.append(post)
        cls.user_list = []
        for i in range(5):
            user = User.objects.create_user(username=f"user_{i}", password=f"user_{i}")
            Post.objects.create(owner=user, content=f"content_{i}")
            cls.user_list.append(user)

        cls.follower = cls.user_list[:3]
        for user in cls.follower:
            Follow.objects.create(follower=user, following=cls.basic_user)
        cls.following = cls.user_list[2:]
        for user in cls.following:
            Follow.objects.create(follower=cls.basic_user, following=user)

    def test_get_all_user(self):
        # 본인 제외 전체 유저 검색
        self.client.force_login(self.basic_user)
        res = self.client.get(reverse("user-list"))
        data = res.data
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        all_users = User.objects.all()
        self.assertEqual(len(data), len(all_users) - 1)
        id_list = [user["pk"] for user in data]
        self.assertNotIn(self.basic_user.pk, id_list)

        # 로그인 하지 않았을 때
        self.client.logout()
        res = self.client.get(reverse("user-list"))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_post_created_by_user(self):
        # 본인이 작성한 개시물 검색
        self.client.force_login(self.basic_user)
        res = self.client.get(reverse("user-posts"))
        data = res.data
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.basic_user_posts), len(data))

        # 로그인 하지 않았을 때
        self.client.logout()
        res = self.client.get(reverse("user-posts"))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PostTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.basic_user = User.objects.create_user(username="basic", password="basic")
        cls.basic_user_posts = []
        for i in range(5):
            post = Post.objects.create(owner=cls.basic_user, content=f"content_{i}")
            cls.basic_user_posts.append(post)
        cls.user_list = []
        for i in range(5):
            user = User.objects.create_user(username=f"user_{i}", password=f"user_{i}")
            cls.user_list.append(user)

        cls.follower = cls.user_list[:3]
        for user in cls.follower:
            Follow.objects.create(follower=user, following=cls.basic_user)
            for i in range(3):
                post = Post.objects.create(owner=user, content=f"{user}_{i}")

        cls.following = cls.user_list[2:]
        for user in cls.following:
            Follow.objects.create(follower=cls.basic_user, following=user)
            for i in range(3):
                post = Post.objects.create(owner=user, content=f"{user}_{i}")

    def test_get_all_follower_post(self):
        # 팔로우한 유저의 개시물 검색
        self.client.force_login(self.basic_user)
        res = self.client.get(reverse("post-list"))
        data = res.data
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        user_list = [post["owner"]["pk"] for post in data]
        for id in user_list:
            self.assertIn(id, [user.pk for user in self.following])

        # 로그인 하지 않았을 때
        self.client.logout()
        res = self.client.get(reverse("post-list"))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_write_post(self):
        # 일반 개시물 작성
        self.client.force_login(self.basic_user)
        res = self.client.post(reverse("post-list"), {"content": "test content"})
        data = res.data
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data["content"], "test content")
        self.assertEqual(data["owner"]["pk"], self.basic_user.pk)

        # 로그인 하지 않았을 때
        self.client.logout()
        res = self.client.post(reverse("post-list"), {"content": "test content"})
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    @patch("utils.image.upload")
    def test_write_post(self, upload_image_mock: MagicMock):
        # 이미지 생성
        image = PImage.new("RGB", (100, 100))
        byte_array = BytesIO()
        image.save(byte_array, format="JPEG")
        image_data = byte_array.getvalue()
        image = SimpleUploadedFile(
            name="test_image.jpg",
            content=image_data,
            content_type="image/jpeg",
        )

        img_url = "https://test.com/test.jpg"
        upload_image_mock.return_value = img_url
        data = {"content": "image content", "image": image}

        # 이미지가 있는 개시물 작성
        self.client.force_login(self.basic_user)
        res = self.client.post(reverse("post-list"), data)
        data = res.data
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data["content"], "image content")
        self.assertEqual(data["owner"]["pk"], self.basic_user.pk)
        self.assertEqual(data["image"], img_url)

        # 로그인 하지 않았을 때
        self.client.logout()
        data = {"content": "image content", "image": image}
        res = self.client.post(reverse("post-list"), data)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_post(self):
        # 개시물 업데이트
        self.client.force_login(self.basic_user)
        post = Post.objects.create(owner=self.basic_user, content="test content")
        data = {"content": "update content"}
        res = self.client.put(reverse("post-detail", args=[post.pk]), data)
        data = res.data
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(data["id"], post.pk)
        self.assertEqual(data["content"], "update content")
        self.assertEqual(data["owner"]["pk"], self.basic_user.pk)

        # 다른 유저 개시물 업데이트
        self.client.force_login(self.basic_user)
        first = User.objects.create(username="first", password="first")
        post = Post.objects.create(owner=first, content="test content")
        data = {"content": "update content"}
        res = self.client.put(reverse("post-detail", args=[post.pk]), data)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        # 로그인 하지 않았을 때
        self.client.logout()
        second = User.objects.create(username="second", password="second")
        post = Post.objects.create(owner=second, content="test content")
        data = {"content": "update content"}
        res = self.client.put(reverse("post-detail", args=[post.pk]), data)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    @patch("utils.image.upload")
    def test_update_post_with_image(self, upload_image_mock: MagicMock):
        # 이미지 생성
        image = PImage.new("RGB", (100, 100))
        byte_array = BytesIO()
        image.save(byte_array, format="JPEG")
        image_data = byte_array.getvalue()
        image = SimpleUploadedFile(
            name="test_image.jpg",
            content=image_data,
            content_type="image/jpeg",
        )

        img_url = "https://test.com/test.jpg"
        upload_image_mock.return_value = img_url

        # 이미지 있는 개시물 업데이트
        self.client.force_login(self.basic_user)
        post = Post.objects.create(owner=self.basic_user, content="test content")
        data = {"content": "update content", "image": image}
        res = self.client.put(reverse("post-detail", args=[post.pk]), data)
        data = res.data
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(data["id"], post.pk)
        self.assertEqual(data["content"], "update content")
        self.assertEqual(data["owner"]["pk"], self.basic_user.pk)
        self.assertEqual(data["image"], img_url)

        # 다른 유저 개시물 업데이트
        self.client.force_login(self.basic_user)
        first = User.objects.create(username="first", password="first")
        post = Post.objects.create(owner=first, content="test content")
        data = {"content": "update content", "image": image}
        res = self.client.put(reverse("post-detail", args=[post.pk]), data)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        # 로그인 하지 않았을 때
        self.client.logout()
        second = User.objects.create(username="second", password="second")
        post = Post.objects.create(owner=second, content="test content")
        data = {"content": "update content", "image": image}
        res = self.client.put(reverse("post-detail", args=[post.pk]), data)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_post(self):
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
        cls.basic_user = User.objects.create_user(username="basic", password="basic")
        cls.basic_user_posts = []
        for i in range(5):
            post = Post.objects.create(owner=cls.basic_user, content=f"content_{i}")
            cls.basic_user_posts.append(post)
        cls.user_list = []
        for i in range(5):
            user = User.objects.create_user(username=f"user_{i}", password=f"user_{i}")
            cls.user_list.append(user)

        cls.follower = cls.user_list[:3]
        for user in cls.follower:
            Follow.objects.create(follower=user, following=cls.basic_user)
            for i in range(3):
                post = Post.objects.create(owner=user, content=f"{user}_{i}")

        cls.following = cls.user_list[2:]
        for user in cls.following:
            Follow.objects.create(follower=cls.basic_user, following=user)
            for i in range(3):
                post = Post.objects.create(owner=user, content=f"{user}_{i}")


#     def test_get_all_following(self):
#         self.client.force_login(self.basic_user)
#         res = self.client.get(reverse("follow-list"))
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         data = json.loads(res.content)
#         follow_list = Follow.objects.filter(user=self.basic_user).all()
#         serializer = FollowSerializer(follow_list, many=True)
#         self.assertEqual(data, serializer.data)

#     def test_get_all_followers(self):
#         self.client.force_login(self.basic_user)
#         res = self.client.get(reverse("follow-follower"))
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         data = json.loads(res.content)
#         follower_list = Follow.objects.filter(follow=self.basic_user).all()
#         serializer = FollowSerializer(follower_list, many=True)
#         self.assertEqual(data, serializer.data)

#     def test_follow(self):
#         # 정상 요청
#         self.client.force_login(self.basic_user)
#         test_user = Follow.objects.exclude(user=self.basic_user).first().user
#         res = self.client.post(reverse("follow-list"), {"follow": test_user.pk})
#         self.assertEqual(res.status_code, status.HTTP_201_CREATED)
#         data = json.loads(res.content)
#         self.assertEqual(data["user"]["pk"], self.basic_user.pk)
#         self.assertEqual(data["follow"]["pk"], test_user.pk)

#         # 이미 팔로우
#         self.client.force_login(self.basic_user)
#         follow = Follow.objects.filter(user=self.basic_user).first().follow
#         res = self.client.post(reverse("follow-list"), {"follow": follow.pk})
#         self.assertEqual(res.status_code, status.HTTP_302_FOUND)

#         # 본인과 팔로우
#         self.client.force_login(self.basic_user)
#         res = self.client.post(reverse("follow-list"), {"follow": self.basic_user.pk})
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_unfollow(self):
#         # 존재하는 팔로우 삭제
#         self.client.force_login(self.basic_user)
#         follow = Follow.objects.filter(user=self.basic_user).first().follow
#         res = self.client.delete(reverse("follow-detail", args=[follow.pk]))
#         self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

#         # 존재하지 않는 팔로우 삭제
#         self.client.force_login(self.basic_user)
#         follow = Follow.objects.exclude(user=self.basic_user).first().follow
#         res = self.client.delete(reverse("follow-detail", args=[follow.pk]))
#         self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
