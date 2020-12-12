from django.urls import path

from . import views


urlpatterns = [
    path(
        "v1/subscriptions/<int:pk>/",
        views.SubscriptionDeleteAPIView.as_view(),
        name="delete-subscription",
    ),
    path(
        "v1/subscriptions/",
        views.SubscriptionCreateAPIView.as_view(),
        name="create-subscription",
    ),
    path(
        "v1/ingredients/",
        views.IngredientListAPIView.as_view(),
        name="ingredients-list",
    ),
    path(
        "v1/favorites/<int:pk>/",
        views.FavoriteDeleteAPIView.as_view(),
        name="delete-favorite",
    ),
    path(
        "v1/favorites/",
        views.FavoriteCreateAPIView.as_view(),
        name="create-favorite",
    ),
    path(
        "v1/purchases/",
        views.ShoppingListCreateAPIView.as_view(),
        name="purchases_list",
    ),
    path(
        "v1/purchases/<int:pk>/",
        views.ShoppingListDeleteAPIView.as_view(),
        name="purchase_delete",
    ),
]
