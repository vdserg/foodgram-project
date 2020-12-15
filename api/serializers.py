from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

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
    id = serializers.SlugRelatedField(
        slug_field="id", queryset=User.objects.all(), source="author"
    )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Subscription
        fields = ["id", "user"]
        validators = [
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(), fields=["id", "user"]
            )
        ]


class FavoriteSerializer(serializers.ModelSerializer):
    id = serializers.SlugRelatedField(
        slug_field="id", queryset=Recipe.objects.all(), source="recipe"
    )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Favorite
        fields = ["id", "user"]
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(), fields=["id", "user"]
            )
        ]


class ShoppingListSerializer(serializers.ModelSerializer):
    id = serializers.SlugRelatedField(
        slug_field="id", queryset=Recipe.objects.all(), source="recipe"
    )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ShoppingList
        fields = ["id", "user"]
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingList.objects.all(), fields=["id", "user"]
            )
        ]
