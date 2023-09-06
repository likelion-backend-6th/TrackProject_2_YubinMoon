from django.db import models
from django.contrib.auth.models import User


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    follow = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followed_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["follow"]),
        ]

    def __str__(self):
        return f"{self.user} follows {self.follow}"


class Image(models.Model):
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.url}"


class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["owner"]),
        ]

    def __str__(self):
        return f"{self.owner} at {self.created_at}"
