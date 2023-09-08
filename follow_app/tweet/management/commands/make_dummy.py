from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tweet.models import Follow, Post


class Command(BaseCommand):
    def handle(self, **options):
        # if db has user script doesn't work
        if User.objects.filter(username="user0").exists():
            print("데이터가 이미 존재합니다.")
            exit(0)

        # create user data
        for i in range(5):
            user = User.objects.create_user(username=f"user{i}", password=f"user{i}")
            # create post data
            for j in range(3):
                Post.objects.create(owner=user, content=f"{j}. post by user{i}")

        # set follow data
        for i in range(5):
            user = User.objects.get(username=f"user{i}")
            a = (i + 1) % 5
            b = (i + 2) % 5
            c = (i + 4) % 5
            usera = User.objects.get(username=f"user{a}")
            userb = User.objects.get(username=f"user{b}")
            userc = User.objects.get(username=f"user{c}")
            Follow.objects.create(user=user, follow=usera)
            Follow.objects.create(user=user, follow=userb)
            Follow.objects.create(user=user, follow=userc)

        print("데이터 생성 완료")
