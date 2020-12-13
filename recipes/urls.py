from django.urls import path

from . import views

app_name = "recipes"
urlpatterns = [
    path("", views.RecipeList.as_view(), name="index"),
    path("recipe/<int:pk>/", views.RecipeDetail.as_view(), name="recipe"),
    path(
        "recipe/author/<str:username>/",
        views.AuthorRecipeList.as_view(),
        name="author",
    ),
    path("recipe/new/", views.RecipeCreateView.as_view(), name="new_recipe"),
    path(
        "recipe/<int:pk>/edit/",
        views.RecipeUpdateView.as_view(),
        name="recipe_edit",
    ),
    path(
        "recipe/<int:pk>/delete/",
        views.RecipeDeleteView.as_view(),
        name="recipe_delete",
    ),
    path(
        "subscription/",
        views.SubscriptionListView.as_view(),
        name="subscription_list",
    ),
    path(
        "recipe/favorite/", views.FavoriteListView.as_view(), name="favorite"
    ),
    path(
        "shopping_cart/",
        views.ShoppingCartListView.as_view(),
        name="shopping_cart",
    ),
    path(
        "shopping_cart/download/",
        views.ShoppingListDownload.as_view(),
        name="shopping_list_download",
    ),
]
