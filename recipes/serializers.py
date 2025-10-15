from rest_framework import serializers
from .models import Category, Recipe

class CategorySerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')  # show username instead of ID

    class Meta:
        model = Category
        fields = ['id', 'name', 'author', 'author_username']
        read_only_fields = ['author', 'author_username']  # author set automatically


class RecipeSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')  # show username instead of ID
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'category', 'category_name', 'image', 'author', 'author_username', 'created_at', 'updated_at']
        read_only_fields = ['author', 'author_username', 'category_name']  # author is set automatically
