from django.urls import include, path

from . import views

urlpatterns = [
    path(
        "v1/",
        include(
            [
                path(
                    "subscriptions/<int:pk>/",
                    views.SubscriptionDeleteAPIView.as_view(),
                    name="delete-subscription",
                ),
                path(
                    "subscriptions/",
                    views.SubscriptionCreateAPIView.as_view(),
                    name="create-subscription",
                ),
                path(
                    "ingredients/",
                    views.IngredientListAPIView.as_view(),
                    name="ingredients-list",
                ),
                path(
                    "favorites/<int:pk>/",
                    views.FavoriteDeleteAPIView.as_view(),
                    name="delete-favorite",
                ),
                path(
                    "favorites/",
                    views.FavoriteCreateAPIView.as_view(),
                    name="create-favorite",
                ),
                path(
                    "purchases/",
                    views.ShoppingListCreateAPIView.as_view(),
                    name="purchases_list",
                ),
                path(
                    "purchases/<int:pk>/",
                    views.ShoppingListDeleteAPIView.as_view(),
                    name="purchase_delete",
                ),
            ]
        ),
    )
]
