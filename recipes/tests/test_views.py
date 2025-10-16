from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from user.models import CustomUser
from recipes.models import Category, Recipe


class RecipesViewTests(APITestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(username="user1", email="user1@example.com", password="pass1234")
        self.user2 = CustomUser.objects.create_user(username="user2", email="user2@example.com", password="pass1234")
        self.client.force_authenticate(user=self.user1)

        # Create sample categories and recipes
        self.category1 = Category.objects.create(name="Desserts", author=self.user1)
        self.category2 = Category.objects.create(name="Salads", author=self.user2)
        self.recipe1 = Recipe.objects.create(
            title="Cake", description="Sweet cake", category=self.category1, author=self.user1
        )
        self.recipe2 = Recipe.objects.create(
            title="Salad", description="Fresh salad", category=self.category2, author=self.user2
        )

    # -------- Category Tests --------
    def test_list_all_categories(self):
        url = reverse("category-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_my_categories_list_create(self):
        url = reverse("my-categories")
        # GET
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        # POST
        response = self.client.post(url, {"name": "Drinks"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Drinks")
        self.assertEqual(response.data["author_username"], "user1")

    def test_category_update_delete_permission(self):
        # Try to update category owned by self
        url = reverse("category-detail", args=[self.category1.id])
        response = self.client.patch(url, {"name": "UpdatedDessert"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Try to update category owned by someone else
        url = reverse("category-detail", args=[self.category2.id])
        response = self.client.patch(url, {"name": "Hacked"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # -------- Recipe Tests --------
    def test_list_all_recipes(self):
        url = reverse("recipe-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_my_recipes_list_create(self):
        url = reverse("my-recipes")
        # GET
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        # POST
        response = self.client.post(url, {"title": "Pie", "description": "Tasty pie", "category": self.category1.id}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Pie")
        self.assertEqual(response.data["author_username"], "user1")

    def test_recipe_update_delete_permission(self):
        # Update own recipe
        url = reverse("recipe-detail", args=[self.recipe1.id])
        response = self.client.patch(url, {"title": "UpdatedCake"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Update other's recipe
        url = reverse("recipe-detail", args=[self.recipe2.id])
        response = self.client.patch(url, {"title": "HackedSalad"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
