from django.db import models
from user.models import CustomUser  # link to our custom user model

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    author = models.ForeignKey(CustomUser, related_name='categories', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, related_name='recipes', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    author = models.ForeignKey(CustomUser, related_name='recipes', on_delete=models.CASCADE)  # <-- owner
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
