from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    ShoppingList,
    Subscription,
)
from .serializers import (
    FavoriteSerializer,
    IngredientSerializer,
    ShoppingListSerializer,
    SubscriptionSerializer,
    User,
)


class IngredientListAPIView(ListAPIView):
    serializer_class = IngredientSerializer

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        query = self.request.query_params.get("query")

        return queryset.filter(title__istartswith=query)


class SubscriptionCreateAPIView(CreateAPIView):
    serializer_class = SubscriptionSerializer


class SubscriptionDeleteAPIView(DestroyAPIView):
    serializer_class = SubscriptionSerializer
    queryset = User.objects.all()

    def destroy(self, request, *args, **kwargs):
        Subscription.objects.filter(
            user=self.request.user, author=self.get_object()
        ).delete()
        return Response(data={"success": True})


class FavoriteCreateAPIView(CreateAPIView):
    serializer_class = FavoriteSerializer


class FavoriteDeleteAPIView(DestroyAPIView):
    serializer_class = FavoriteSerializer
    queryset = Recipe.objects.all()

    def destroy(self, request, *args, **kwargs):
        Favorite.objects.filter(
            user=self.request.user, recipe=self.get_object()
        ).delete()
        return Response(data={"success": True})


class ShoppingListCreateAPIView(CreateAPIView):
    serializer_class = ShoppingListSerializer


class ShoppingListDeleteAPIView(DestroyAPIView):
    serializer_class = ShoppingListSerializer
    queryset = ShoppingList.objects.all()

    def delete(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=kwargs.get("pk"))
        recipe_in_cart = recipe.in_shopping_list.filter(user=request.user)
        if recipe_in_cart.delete():
            return Response({"success": True})
        return Response({"success": False})
