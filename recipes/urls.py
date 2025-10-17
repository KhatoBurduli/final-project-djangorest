from django.urls import path
from .views import RecipeListView, MyRecipeListCreateView, RecipeDetailView, RecipesByCategoryView
from .views import CategoryListView, MyCategoryListCreateView, CategoryDetailView

urlpatterns = [
    # Categories
    path('categories/', CategoryListView.as_view(), name='category-list'),  # GET all categories
    path('categories/my/', MyCategoryListCreateView.as_view(), name='my-categories'),  # GET & POST for own categories
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),  # GET/PUT/PATCH/DELETE

    # Recipes
    path('recipes/', RecipeListView.as_view(), name='recipe-list'),  # /api/recipes/
    path('recipes/my/', MyRecipeListCreateView.as_view(), name='my-recipes'),  # /api/recipes/my/
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),  # /api/recipes/<id>/
    path('recipes/category/<int:category_id>/', RecipesByCategoryView.as_view(), name='recipes-by-category'),
]
