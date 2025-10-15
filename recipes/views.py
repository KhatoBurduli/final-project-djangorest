from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied

from .models import Category, Recipe
from .serializers import CategorySerializer, RecipeSerializer

# Category CRUD
# List all categories (any logged-in user can see)
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


# List and create categories belonging to logged-in user
class MyCategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# Retrieve, update, delete a single category (only author can edit/delete)
class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        if self.get_object().author != self.request.user:
            raise PermissionDenied("You can only edit categories you created.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("You can only delete categories you created.")
        instance.delete()

# Recipe CRUD
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Recipe
from .serializers import RecipeSerializer

# List all recipes (read-only for logged-in users)
class RecipeListView(generics.ListAPIView):
    queryset = Recipe.objects.select_related('author').all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]


# List and create recipes belonging to the logged-in user
class MyRecipeListCreateView(generics.ListCreateAPIView):
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Recipe.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# Retrieve, update, delete a single recipe (only author can edit/delete)
class RecipeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        if self.get_object().author != self.request.user:
            raise PermissionDenied("You can only edit your own recipes.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("You can only delete your own recipes.")
        instance.delete()
