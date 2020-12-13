from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    ShoppingList,
    Subscription,
)

User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["title", "dimension"]


class SubscriptionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Subscription
        fields = ["id"]

    def validate(self, attrs):
        author_id = attrs.get("id")
        author = get_object_or_404(User, id=author_id)
        user = self.context.get("request").user

        if user == author:
            raise serializers.ValidationError(
                {"detail": "Вы не можете подписаться на себя"}
            )

        if Subscription.objects.filter(user=user, author=author).exists():
            raise serializers.ValidationError(
                {"detail": "Вы уже подписаны на этого автора"}
            )

        attrs["user"] = user
        attrs["author"] = author
        return super(SubscriptionSerializer, self).validate(attrs)


class FavoriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Favorite
        fields = ["id"]

    def validate(self, attrs):
        recipe_id = attrs.get("id")
        recipe = get_object_or_404(Recipe, id=recipe_id)
        user = self.context.get("request").user

        if Favorite.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError(
                {"detail": "Этот рецепт уже у вас в избранном"}
            )

        attrs["user"] = user
        attrs["recipe"] = recipe
        return super(FavoriteSerializer, self).validate(attrs)


class ShoppingListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = ShoppingList
        fields = ["id"]

    def validate(self, attrs):
        recipe_id = attrs.get("id")
        recipe = get_object_or_404(Recipe, id=recipe_id)
        user = self.context.get("request").user

        if ShoppingList.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError(
                {"detail": "Этот рецепт уже в списке покупок"}
            )

        attrs["user"] = user
        attrs["recipe"] = recipe
        return super(ShoppingListSerializer, self).validate(attrs)
