from django.test import TestCase
from recipes.serializers import CategorySerializer, RecipeSerializer
from recipes.models import Category, Recipe
from user.models import CustomUser


class CategorySerializerTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="john", password="StrongPass123!")

    def test_category_serializer_valid(self):
        category = Category.objects.create(name="Desserts", author=self.user)
        serializer = CategorySerializer(category)
        data = serializer.data
        self.assertEqual(data["name"], "Desserts")
        self.assertEqual(data["author_username"], "john")


class RecipeSerializerTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="john", password="StrongPass123!")
        self.category = Category.objects.create(name="Desserts", author=self.user)

    def test_recipe_serializer_valid(self):
        recipe = Recipe.objects.create(
            title="Cake",
            description="Tasty cake",
            category=self.category,
            author=self.user
        )
        serializer = RecipeSerializer(recipe)
        data = serializer.data
        self.assertEqual(data["title"], "Cake")
        self.assertEqual(data["author_username"], "john")
        self.assertEqual(data["category_name"], "Desserts")
