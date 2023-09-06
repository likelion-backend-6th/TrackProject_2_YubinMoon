import json
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase

from .models import Follow, Image, Post


# Create your tests here.
class PostTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.basic_user = User.objects.create(username="basic", password="basic")
        cls.follow_user = User.objects.create(username="follower", password="follower")
        cls.not_follow_user_list = []
        for i in range(5):
            user = User.objects.create(
                username=f"un_follow_{i}", password=f"un_follow_{i}"
            )
            Follow.objects.create(user=cls.follow_user, follow=user)
            cls.not_follow_user_list.append(user)
        cls.follow_user_list = []
        for i in range(5):
            user = User.objects.create(username=f"follow_{i}", password=f"follow_{i}")
            Follow.objects.create(user=cls.basic_user, follow=user)
            Follow.objects.create(user=cls.follow_user, follow=user)
            Follow.objects.create(user=user, follow=cls.follow_user)
            cls.follow_user_list.append(user)

        for i in range(5):
            Post.objects.create(owner=cls.basic_user, content=f"content_{i}")
        for i in range(5):
            Post.objects.create(owner=cls.follow_user, content=f"content_{i}")

    def test_get_all_user(self):
        self.client.force_login(self.basic_user)
        res = self.client.get(reverse("user-list"))
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        all_users = User.objects.all()
        self.assertEqual(len(data), len(all_users) - 1)

    # def test_get_all_post_created_by_user(self):
    #     self.client.force_login(self.basic_user)
    #     res = self.client.get(reverse("post-posts"))
    #     self.assertEqual(res.status_code, 200)
    #     data = json.loads(res.content)
    #     user_posts = Post.objects.filter(owner=self.basic_user)
    #     self.assertEqual(len(data), len(user_posts))
